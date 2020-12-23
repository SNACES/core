from src.dao.cluster.setter.cluster_setter import ClusterSetter
from src.dao.cluster.setter.mongo_cluster_setter import MongoClusterSetter
from src.dao.cluster.getter.cluster_getter import ClusterGetter
from src.dao.cluster.getter.mongo_cluster_getter import MongoClusterGetter
from src.shared.mongo import get_collection_from_config
from typing import Dict


class ClusterDAOFactory():
    def create_getter(config: Dict) -> ClusterGetter:
        cluster_getter = None
        if config["type"] == "Mongo":
            cluster_getter = MongoClusterGetter()
            collection = get_collection_from_config(config["config"])
            cluster_getter.set_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return cluster_getter

    def create_setter(config: Dict) -> ClusterSetter:
        cluster_setter = None
        if config["type"] == "Mongo":
            cluster_setter = MongoClusterSetter()
            collection = get_collection_from_config(config["config"])
            cluster_setter.set_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return cluster_setter
