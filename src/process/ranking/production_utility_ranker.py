from src.model.ranking import Ranking
from src.process.ranking.ranker import Ranker
from typing import List
from tqdm import tqdm

class ProductionUtilityRanker(Ranker):
    def __init__(self, cluster_getter, raw_tweet_getter, ranking_setter):
        self.cluster_getter = cluster_getter
        self.raw_tweet_getter = raw_tweet_getter
        self.ranking_setter = ranking_setter
        self.ranking_function_name = "retweets"

    def score_users(self, user_ids: List[str]):
        scores = {}
        for id in user_ids:
            scores[str(id)] = 0

        for id in tqdm(user_ids):
            retweets = self.raw_tweet_getter.get_retweets_of_user_by_user_id_time_restricted(id)
            #retweets = self.raw_tweet_getter.get_retweets_of_user_by_user_id(id)

            for retweet in retweets:
                # print(str(str(retweet.user_id) in user_ids) + " " + str(str(retweet.user_id) == id))
                if str(retweet.user_id) in user_ids and str(retweet.user_id) != str(id):
                    scores[str(id)] += 1

        return scores
