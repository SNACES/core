from src.model.ranking import Ranking
from typing import List


class Ranker():
    def __init__(self, cluster_getter, user_getter, ranking_setter):
        self.cluster_getter = cluster_getter
        self.raw_tweet_getter = raw_tweet_getter
        self.ranking_setter = ranking_setter
        self.ranking_function_name = None

    def rank(self, seed_id, params):
        clusters, cluster_params = self.cluster_getter.get_clusters(seed_id, params)

        cluster = clusters[0]
        user_ids = cluster.users

        scores = self.score_users(user_ids)

        ranked_ids = list(sorted(scores, key=scores.get))
        ranking = Ranking(seed_id, ranked_ids, self.ranking_function_name, cluster_params)

        self.ranking_setter.store_ranking(ranking)

    def score_users(self, user_ids: List[str]):
        raise NotImplementedError("This method should be implemented by subclasses")
