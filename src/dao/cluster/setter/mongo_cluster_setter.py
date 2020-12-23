from src.dao.cluster.setter.cluster_setter import ClusterSetter
from src.model.cluster import Cluster
from typing import List
import bson


class MongoClusterSetter(ClusterSetter):
    def __init__(self):
        self.collection = None

    def set_collection(self, collection) -> None:
        self.collection = collection

    def store_clusters(self, seed_id: str, clusters: List[Cluster], params):
        if self._contains_cluster(seed_id, params):
            pass
        else:
            self.collection.insert_one({"seed_id": int(seed_id),
                "params": params,
                "clusters": [cluster.__dict__ for cluster in clusters]})

    def _contains_cluster(self, seed_id, params):
        return self.collection.find_one({"seed_id": bson.int64.Int64(seed_id), "params": params}) is not None
