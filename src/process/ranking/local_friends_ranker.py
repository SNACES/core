from src.process.ranking.ranker import Ranker
from typing import List


class LocalFriendsRanker(Ranker):
    def __init__(self, cluster_getter, friends_getter, ranking_setter):
        self.cluster_getter = cluster_getter
        self.ranking_setter = ranking_setter
        self.ranking_function_name = "local_friends"
        self.friends_getter = friends_getter

    def score_users(self, user_ids: List[str]):
        scores = {}
        for user in user_ids:
            score = 0
            friends = self.friends_getter.get_user_friends_ids(user)
            for cluster_user in user_ids:
                # if a user in the cluster is friend with user
                if cluster_user in friends:
                    score += 1
            scores[user] = score

        return scores
