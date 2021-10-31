from src.model.ranking import Ranking
from src.process.ranking.ranker import Ranker
from typing import List
from tqdm import tqdm

class ProductionUtilityRanker(Ranker):
    """the number of times a tweet by u has been retweeted by users in the cluster."""
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
            # retweets by user_id that has retweet_user_id(original tweet)
            retweets = self.raw_tweet_getter.get_retweets_of_user_by_user_id_time_restricted(id)

            for retweet in retweets:
                # original user
                writer = retweet.retweet_user_id
                # if original user in the cluster and is not the user itself
                if str(writer) in user_ids and str(writer) != str(id):
                    scores[str(writer)] += 1

        return scores
