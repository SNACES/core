from src.process.community_ranking.community_ranker import CommunityRanker
from typing import List


class CommunityFollowerRanker(CommunityRanker):
    def __init__(self, user_getter):
        self.user_getter = user_getter
        self.ranking_function_name = "follower"

    def score_users(self, user_ids: List[str], current_community):
        users = self.user_getter.get_users_by_id_list(user_ids)


        scores = {}
        for user in users:
            if user is not None:
                scores[user.id] = user.followers_count
            #else:
                #scores[user.id] = 0

        return scores
