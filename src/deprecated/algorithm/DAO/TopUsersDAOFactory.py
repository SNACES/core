from src.algorithm.Mongo_Getter_Setter.MongoCluster.MongoClusterGetter import MongoClusterGetter
from src.algorithm.Mongo_Getter_Setter.MongoRelativeWordFreq.MongoRelativeWordFrequencyGetter import MongoRelativeWordFrequencyGetter
from src.algorithm.Mongo_Getter_Setter.MongoTopWords.MongoTopWordsGetter import MongoTopWordsGetter
from src.algorithm.Mongo_Getter_Setter.MongoTopUsers.MongoTopUsersSetter import MongoTopUsersSetter
from typing import Dict, List
from src.shared.mongo import get_collection_from_config


class TopUsersDAOFactory():
    def create_cluster_getter(config: Dict):
        cluster_getter = None
        if config["type"] == "Mongo":
            cluster_getter = MongoClusterGetter()
            collection = get_collection_from_config(config["config"])
            cluster_getter.set_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return cluster_getter

    def create_wordfrequency_getter(config: Dict):
        relative_wordfrequency_getter = None
        if config["type"] == "Mongo":
            relative_wordfrequency_getter = MongoRelativeWordFrequencyGetter()
            collection = get_collection_from_config(config["config"])
            relative_wordfrequency_getter.set_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return relative_wordfrequency_getter  

    def create_topwords_getter(config: Dict):
        top_words_getter = None
        if config["type"] == "Mongo":
            top_words_getter = MongoTopWordsGetter()
            collection = get_collection_from_config(config["config"])
            top_words_getter.set_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return top_words_getter  

    def create_topusers_setter(config: Dict):
        top_users_setter = None
        if config["type"] == "Mongo":
            top_users_setter = MongoTopUsersSetter()
            collection = get_collection_from_config(config["config"])
            top_users_setter.set_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return top_users_setter