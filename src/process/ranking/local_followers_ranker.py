from src.model.ranking import Ranking
from src.process.ranking.ranker import Ranker
from typing import List


class LocalFollowerRanker(Ranker):
    def __init__(self, cluster_getter, user_getter, ranking_setter, friends_getter):
        self.cluster_getter = cluster_getter
        self.user_getter = user_getter
        self.ranking_setter = ranking_setter
        self.ranking_function_name = "local_followers"
        self.friends_getter = friends_getter

    def score_users(self, user_ids: List[str]):
        users = self.user_getter.get_users_by_id_list(user_ids)
        scores = {}

        user_friends = {}
        for user in user_ids:
            user_friends[user] = self.friends_getter.get_user_friends_ids(user)
        for user in users:
            local_followers = 0
            for friend in user_ids:
                if str(user.id) in user_friends[friend]:
                    local_followers += 1
            scores[str(user.id)] = local_followers

        return scores
