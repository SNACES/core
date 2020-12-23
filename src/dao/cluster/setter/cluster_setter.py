from src.model.cluster import Cluster
from typing import Dict

class ClusterSetter:
    def store_cluster(self, cluster: Cluster):
        raise NotImplementedError("Subclasses should implement this")
