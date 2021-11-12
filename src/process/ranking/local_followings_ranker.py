from src.process.ranking.ranker import Ranker
from typing import List


class LocalFollowingsRanker(Ranker):
    def __init__(self, cluster_getter, followers_getter, ranking_setter):
        self.cluster_getter = cluster_getter
        self.ranking_setter = ranking_setter
        self.ranking_function_name = "local_followings"
        self.followers_getter = followers_getter

    def score_users(self, user_ids: List[str]):
        scores = {}
        for user_id in user_ids:
            scores[str(user_id)] = 0
        for user in user_ids:
            followers = self.followers_getter.get_follower_by_id(user)
            for cluster_user in user_ids:
                # user is following a user in the cluster
                if cluster_user in followers:
                    scores[cluster_user] += 1
        return scores
