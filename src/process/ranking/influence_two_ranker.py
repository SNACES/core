from src.process.ranking.ranker import Ranker
from typing import Dict, List
from tqdm import tqdm

class InfluenceTwoRanker(Ranker):
	def __init__(self, raw_tweet_getter, friends_getter, ranking_setter):
		self.raw_tweet_getter = raw_tweet_getter
		self.friends_getter = friends_getter
		self.ranking_setter = ranking_setter
		self.ranking_function_name = "influence two"

	def create_friends_dict(self, user_ids):
		friends = {}
		for user_id in user_ids:
			friends_of_user_id = self.friends_getter.get_user_friends_ids(user_id)
			friends[user_id] = [str(id) for id in friends_of_user_id]
		return friends

	def score_users(self, user_ids: List[str]):
		# Score users by summing up the percentage of tweets they make up in all followers' retweets
		scores = {user_id: 0 for user_id in user_ids} # Initialize all scores to 0

		tweets = self.raw_tweet_getter.get_tweets_by_user_ids(user_ids)
		valid_tweets = [tweet for tweet in tweets if tweet.retweet_user_id != tweet.user_id]

		# Define helper functions
		tweets_by_retweet_group = self._group_by_retweet_id(valid_tweets)
		def get_retweets_of_tweet_id(tweet_id):
			return tweets_by_retweet_group.get(str(tweet_id), [])
		def get_later_retweets_of_tweet_id(tweet_id, created_at):
			return [tweet for tweet in get_retweets_of_tweet_id(tweet_id) if tweet.created_at > created_at]
		
		retweets_by_retweeter = self._group_by_retweeter(valid_tweets)
		def get_num_retweets_by(id):
			return len(retweets_by_retweeter.get(id, []))
		
		friends = self.create_friends_dict(user_ids)
		def is_direct_follower(a, b): # 'b' is a follower of 'a'
			return a in friends.get(b, [])
			
		for id in tqdm(user_ids):
			user_tweets = [tweet for tweet in valid_tweets if str(tweet.user_id) == id]
			user_original_tweets = [tweet for tweet in user_tweets if tweet.retweet_id is None]
			user_retweets = [tweet for tweet in user_tweets if tweet.retweet_id is not None]

			for follower_id in [other_id for other_id in user_ids if id != other_id and is_direct_follower(id, other_id)]:
				follower_score = 0
				# Score original tweets
				for original_tweet in user_original_tweets:
					retweets = get_retweets_of_tweet_id(original_tweet.id)
					follower_score += 1 if any(str(rtw.user_id) == follower_id for rtw in retweets) else 0
				# Score retweets
				for user_retweet in user_retweets:
					retweets = get_later_retweets_of_tweet_id(user_retweet.retweet_id, user_retweet.created_at)
					follower_score += 1 if any(str(rtw.user_id) == follower_id for rtw in retweets) else 0
				
				if get_num_retweets_by(follower_id) > 0:
					follower_score /= get_num_retweets_by(follower_id)
				scores[id] += follower_score
				
		return scores
		
	def _group_by_retweet_id(self, tweets) -> Dict:
		# Puts all tweets with the same retweet_id in the same list
		# Returns: A dictionary where the key is the retweet_id and 
		# the value is the list of tweets with that retweet_id
		dict = {}
		for tweet in tweets:
			key = str(tweet.retweet_id)
			if key in dict:
				dict[key].append(tweet)
			else:
				dict[key] = [tweet]
		
		return dict

	def _group_by_retweeter(self, tweets) -> Dict:
		# Puts all tweets with the same retweeter in the same list
		# Returns: A dictionary where the key is the user_id of the retweeter and 
		# the value is the list of tweets retweeted by the retweeter
		dict = {}
		for tweet in tweets:
			if tweet.retweet_id is None: # tweet is not a retweet
				continue
			key = str(tweet.user_id)
			if key in dict:
				dict[key].append(tweet)
			else:
				dict[key] = [tweet]
		
		return dict

