from src.model.ranking import Ranking
from src.process.ranking.ranker import Ranker
from typing import Dict, List
from tqdm import tqdm

class SocialSupportRanker(Ranker):
    def __init__(self, cluster_getter, raw_tweet_getter, user_getter, ranking_setter, alpha=1.0):
        self.cluster_getter = cluster_getter
        self.raw_tweet_getter = raw_tweet_getter
        self.user_getter = user_getter
        self.ranking_setter = ranking_setter
        self.ranking_function_name = "retweets"
        self.alpha = alpha


    def score_users(self, user_ids: List[str]):
        scores = {user_id: [0, 0] for user_id in user_ids} # Initialize all scores to 0
        tweets = self.raw_tweet_getter.get_tweets_by_user_ids(user_ids)
        # Omit self-retweets
        tweets = [tweet for tweet in tweets if tweet.user_id != tweet.retweet_id]
        tweets_by_retweet_group = self._group_by_retweet_id(tweets)
        def get_retweets_of_tweet_id(tweet_id):
            return tweets_by_retweet_group.get(str(tweet_id), [])

        for id in tqdm(user_ids):
            scores[id][1] = self.user_getter.get_user_by_id(id).followers_count
            user_tweets = [tweet for tweet in tweets if str(tweet.user_id) == id]
            original_tweet_ids = [tweet.id for tweet in user_tweets if tweet.retweet_id is None]
            for original_tweet_id in original_tweet_ids:
                retweets = get_retweets_of_tweet_id(original_tweet_id)
                scores[id][0] += len(retweets)

            retweeted_tweets_ids = [tweet.id for tweet in user_tweets if tweet.retweet_id is not None]
            for retweeted_tweet_id in retweeted_tweets_ids:
                retweets = get_retweets_of_tweet_id(retweeted_tweet_id)
                scores[id][0] += len(retweets) * self.alpha

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
