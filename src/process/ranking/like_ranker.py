from src.process.ranking.ranker import Ranker
from typing import List
from tqdm import tqdm

class LikeRanker(Ranker):
    def __init__(self, cluster_getter, user_getter, ranking_setter):
        self.cluster_getter = cluster_getter
        self.user_getter = user_getter
        self.ranking_setter = ranking_setter
        self.ranking_function_name = "like utility"

    def score_users(self, user_ids: List[str]):
        scores = {}
        for id in user_ids:
            scores[str(id)] = 0

        for id in tqdm(user_ids):
            user = self.user_getter.get_user_by_id(id)
            scores[str(id)] = user.get_likes()
        return scores

