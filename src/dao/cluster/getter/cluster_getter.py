from src.model.cluster import Cluster
from typing import Dict, Optional


class ClusterGetter():
    def get_cluster(self, seed_id: str, params: Optional[Dict] = None) -> Cluster:
        raise NotImplementedError("Subclasses should implement this")
