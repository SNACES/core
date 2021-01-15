from src.model.ranking import Ranking
from typing import Dict, Optional


class RankingGetter():
    def get_ranking(self, seed_id: str, params: Optional[Dict] = None) -> Ranking:
        raise NotImplementedError("Subclasses should implement this")
