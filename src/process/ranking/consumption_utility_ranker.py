from src.model.ranking import Ranking
from src.process.ranking.ranker import Ranker
from typing import List
from tqdm import tqdm

class ConsumptionUtilityRanker(Ranker):
    def __init__(self, cluster_getter, raw_tweet_getter, user_getter, ranking_setter):
        self.cluster_getter = cluster_getter
        self.raw_tweet_getter = raw_tweet_getter
        self.user_getter = user_getter
        self.ranking_setter = ranking_setter
        self.ranking_function_name = "consumption utility"

    def score_users(self, user_ids: List[str]):
        scores = {user_id: [0, 0] for user_id in user_ids} # Initialize all scores to 0
        tweets = self.raw_tweet_getter.get_tweets_by_user_ids(user_ids)
        for tweet in tweets:
            user_id = tweet.user_id
            if tweet.retweet_id is not None and \
                    str(tweet.retweet_user_id) in user_ids and \
                    str(tweet.retweet_user_id) != str(user_id):
                scores[str(user_id)][0] += 1

        for id in tqdm(user_ids):
                scores[id][1] = self.user_getter.get_user_by_id(id).friends_count
                # retweets = self.raw_tweet_getter.get_retweets_by_user_id_time_restricted(id)
                # # coefficient = self.raw_tweet_getter.get_tweet_scale_coefficient(id)
                # for retweet in retweets:
                #     if str(retweet.retweet_user_id) in user_ids and str(retweet.retweet_user_id) != str(id): # retweeting your own tweet does not count
                #         scores[id][0] += 1
                # scores[str(id)] *= coefficient
        return scores
