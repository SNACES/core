from src.model.ranking import Ranking
from src.process.ranking.ranker import Ranker
from typing import List


class FollowerRanker(Ranker):
    def __init__(self, cluster_getter, user_getter, ranking_setter):
        self.cluster_getter = cluster_getter
        self.raw_tweet_getter = raw_tweet_getter
        self.ranking_setter = ranking_setter
        self.ranking_function_name = "followers"

    def score_users(self, user_ids: List[str]):
        users = self.user_getter.get_users_by_id_list(user_ids)

        scores = {}
        for user in users:
            scores[user.id] = user.followers_count

        return scores
