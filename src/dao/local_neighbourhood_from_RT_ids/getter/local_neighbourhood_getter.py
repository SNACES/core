from src.model.local_neighbourhood import LocalNeighbourhood
from typing import Dict, Optional


class LocalNeighbourhoodGetter():
    def get_local_neighbourhood(self, seed_id: str, params: Optional[Dict] = None) -> LocalNeighbourhood:
        raise NotImplementedError("Subclasses should implement this")
