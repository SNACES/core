from src.dao.cluster.getter.cluster_getter import ClusterGetter
from src.model.cluster import Cluster
from typing import Dict
import bson


class MongoClusterGetter():
    def __init__(self):
        self.collection = None

    def set_collection(self, collection) -> None:
        self.collection = collection

    def get_cluster(self, seed_id: str, params=None):
        doc = None
        if params is None:
            doc = self.collection.find_one({"seed_id": bson.int64.Int64(seed_id)})
        else:
            doc = self.collection.find_one({
                "seed_id": bson.int64.Int64(seed_id),
                "params": params})

        return Cluster.fromDict(doc)
