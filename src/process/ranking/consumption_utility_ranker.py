from src.model.ranking import Ranking
from src.process.ranking.ranker import Ranker
from typing import List
from tqdm import tqdm

class ConsumptionUtilityRanker(Ranker):
    def __init__(self, cluster_getter, raw_tweet_getter, ranking_setter):
        self.cluster_getter = cluster_getter
        self.raw_tweet_getter = raw_tweet_getter
        self.ranking_setter = ranking_setter
        self.ranking_function_name = "consumption utility"

    def score_users(self, user_ids: List[str]):
        scores = {}
        for id in user_ids:
            scores[str(id)] = 0

        for id in tqdm(user_ids):
            retweets = self.raw_tweet_getter.get_retweets_by_user_id_time_restricted(id)
            # coefficient = self.raw_tweet_getter.get_tweet_scale_coefficient(id)

            for retweet in retweets:
                if str(retweet.retweet_user_id) in user_ids and str(retweet.retweet_user_id) != str(id): # retweeting your own tweet does not count
                    scores[str(id)] += 1
            # scores[str(id)] *= coefficient
        return scores
