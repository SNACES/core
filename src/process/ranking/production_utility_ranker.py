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
        """
        user_id: is the id of the user <original tweeted the tweet>
        """
        scores = {}
        for user_id in user_ids:
            scores[str(user_id)] = 0

        for user_id in tqdm(user_ids):
            # get tweets tweeted by user_id that is retweeted by others
            retweets = self.raw_tweet_getter.get_retweets_of_user_by_user_id_time_restricted(user_id)

            for retweet in retweets:
                # retweeted user
                retweeter = retweet.user_id
                # if retweeted user in the cluster and is not the user itself
                if str(retweeter) in user_ids and str(retweeter) != str(user_id):
                    scores[user_id] += 1

        return scores
