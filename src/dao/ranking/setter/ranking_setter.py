from typing import List, Dict
from src.model.ranking import Ranking


class RankingSetter:
    """
    An abstract class representing an object that stores tweets in a
    datastore
    """

    def store_ranking(self, ranking: Ranking):
        raise NotImplementedError("Subclasses should implement this")

    def store_rankings(self, rankings: List[Ranking]) -> None:
        for ranking in rankings:
            self.store_ranking(ranking)
