from src.algorithm.Mongo_Getter_Setter.MongoCluster.MongoClusterGetter import MongoClusterGetter
from src.algorithm.Mongo_Getter_Setter.MongoUserFriends.MongoUserNeighborhoodGetter import MongoUserNeighborhoodGetter
from typing import Dict, List
from src.shared.mongo import get_collection_from_config


class CountConnectDAOFactory():
    def create_cluster_getter(config: Dict):
        cluster_getter = None
        if config["type"] == "Mongo":
            cluster_getter = MongoClusterGetter()
            collection = get_collection_from_config(config["config"])
            cluster_getter.set_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return cluster_getter

    def create_friends_getter(config: Dict):
        user_friends_getter = None
        if config["type"] == "Mongo":
            user_friends_getter = MongoUserNeighborhoodGetter()
            collection = get_collection_from_config(config["config"])
            user_friends_getter.set_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return user_friends_getter  
