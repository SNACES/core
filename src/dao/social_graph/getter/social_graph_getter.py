from src.model.social_graph.social_graph import SocialGraph
from typing import Dict, Optional


class SocialGraphGetter():
    def get_social_graph(self, seed_id: str, params: Optional[Dict] = None) -> SocialGraph:
        raise NotImplementedError("Subclasses should implement this")
