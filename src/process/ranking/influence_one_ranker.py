from src.process.ranking.ranker import Ranker
from typing import Dict, List
from tqdm import tqdm


class InfluenceOneRanker(Ranker):
	def __init__(self, raw_tweet_getter, friends_getter, ranking_setter):
		self.raw_tweet_getter = raw_tweet_getter
		self.friends_getter = friends_getter
		self.ranking_setter = ranking_setter
		self.ranking_function_name = "influence one"

	def create_friends_dict(self, user_ids):
		friends = {}
		for user_id in user_ids:
			friends_of_user_id = self.friends_getter.get_user_friends_ids(user_id)
			friends[user_id] = [str(id) for id in friends_of_user_id]
		return friends

	def score_users(self, user_ids: List[str]):
		# Score users with their average number of retweets from direct followers
		friends = self.create_friends_dict(user_ids)
		scores = {user_id: [0,0] for user_id in user_ids} # Initialize all scores to 0

		tweets = self.raw_tweet_getter.get_tweets_by_user_ids(user_ids)
		valid_tweets = [tweet for tweet in tweets if tweet.retweet_user_id != tweet.user_id] # omit self-retweets

		# Define helper functions
		tweets_by_retweet_group = self._group_by_retweet_id(valid_tweets)
		def get_retweets_of_tweet_id(tweet_id):
			return tweets_by_retweet_group.get(str(tweet_id), [])
		def get_later_retweets_of_tweet_id(tweet_id, created_at):
			return [tweet for tweet in get_retweets_of_tweet_id(tweet_id) if tweet.created_at > created_at]
		def is_direct_follower(a, b):
			return a in friends.get(b, [])

		for id in tqdm(user_ids):
			user_tweets = [tweet for tweet in valid_tweets if str(tweet.user_id) == id]

			# Score original tweets
			user_original_tweets = [tweet for tweet in user_tweets if tweet.retweet_id is None]
			for original_tweet in user_original_tweets:
				retweets = get_retweets_of_tweet_id(original_tweet.id)
				retweets_from_direct_followers = [rtw for rtw in retweets if is_direct_follower(id, str(rtw.user_id))]
				scores[id][0] += len(retweets_from_direct_followers)

			# Score retweets
			user_retweets = [tweet for tweet in user_tweets if tweet.retweet_id is not None]
			for user_retweet in user_retweets:
				retweets = get_later_retweets_of_tweet_id(user_retweet.retweet_id, user_retweet.created_at)
				retweets_from_direct_followers = [rtw for rtw in retweets if is_direct_follower(id, str(rtw.user_id))]
				scores[id][0] += len(retweets_from_direct_followers)

			if len(user_tweets) > 0:
				scores[id][0] /= len(user_tweets)
			scores[id][1] = len(user_tweets)
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
