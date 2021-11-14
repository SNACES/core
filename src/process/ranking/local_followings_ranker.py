from src.process.ranking.ranker import Ranker
from typing import List


from src.shared.logger_factory import LoggerFactory

log = LoggerFactory.logger(__name__)
class LocalFollowingsRanker(Ranker):
    def __init__(self, cluster_getter, friendship_getter, ranking_setter):
        self.cluster_getter = cluster_getter
        self.ranking_setter = ranking_setter
        self.ranking_function_name = "local_followings"
        self.friendship_getter = friendship_getter

    def score_users(self, user_ids: List[str]):
        scores = {}
        for user_id in user_ids:
            scores[str(user_id)] = 0
        # for a in range(len(user_ids)):
        #     for b in range(a+1, len(user_ids)):
        #         a_follow_b, b_follow_a = self.friendship_getter.get_friendship_by_id(a, b)
        #         """b is a follower of a"""
        #         if b_follow_a:
        #             scores[str(b)] += 1
        #         if a_follow_b:
        #             scores[str(a)] += 1
        for a in range(len(user_ids)):
            lst = self.friendship_getter.get_user_friends_ids(str(user_ids[a]))
            #log.info(f"friend list: {lst}")
            for b in range(a+1, len(user_ids)):
                #log.info(user_ids[b])
                if int(user_ids[b]) in lst:
                    scores[str(user_ids[a])] += 1
        return scores
