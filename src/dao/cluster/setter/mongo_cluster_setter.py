from src.dao.cluster.setter.cluster_setter import ClusterSetter
from src.model.cluster import Cluster
import bson


class MongoClusterSetter(ClusterSetter):
    def __init__(self):
        self.collection = None

    def set_collection(self, collection) -> None:
        self.collection = collection

    def store_cluster(self, cluster: Cluster):
        if self._contains_cluster(cluster):
            pass
        else:
            self.collection.insert_one(cluster.__dict__)

    def _contains_cluster(self, cluster: Cluster):
        return self.collection.find_one({"seed_id": bson.int64.Int64(cluster.seed_id), "params": cluster.params}) is not None
