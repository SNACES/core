from src.process.ranking.ranker import Ranker
from typing import List


class LocalFollowersRanker(Ranker):
    def __init__(self, cluster_getter, followers_getter, ranking_setter):
        self.cluster_getter = cluster_getter
        self.ranking_setter = ranking_setter
        self.ranking_function_name = "local_followers"
        self.followers_getter = followers_getter

    def score_users(self, user_ids: List[str]):
        scores = {}
        for user in user_ids:
            score = 0
            followers = self.followers_getter.get_follower_by_id(user)
            for cluster_user in user_ids:
                # if a user in the cluster is following user
                if cluster_user in followers:
                    score += 1
            scores[user] = score

        return scores
