from src.dao.cluster_word_frequency.setter.cluster_word_frequency_setter import ClusterWordFrequencySetter
from src.dao.cluster_word_frequency.setter.mongo_cluster_word_frequency_setter import MongoClusterWordFrequencySetter
from src.dao.cluster_word_frequency.getter.cluster_word_frequency_getter import ClusterWordFrequencyGetter
from src.dao.cluster_word_frequency.getter.mongo_cluster_word_frequency_getter import MongoClusterWordFrequencyGetter
from src.shared.mongo import get_collection_from_config
from typing import Dict

class ClusterWordFrequencyDAOFactory():
    def create_setter(config: Dict) -> ClusterWordFrequencySetter:
        cluster_word_frequency_setter = None
        if config["type"] == "Mongo":
            cluster_word_frequency_setter = MongoClusterWordFrequencySetter()
            collection = get_collection_from_config(config["config"])
            cluster_word_frequency_setter.set_user_word_frequency_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return cluster_word_frequency_setter

    def create_getter(config: Dict) -> ClusterWordFrequencyGetter:
        cluster_word_frequency_getter = None
        if config["type"] == "Mongo":
            cluster_word_frequency_getter = MongoClusterWordFrequencyGetter()
            collection = get_collection_from_config(config["config"])
            cluster_word_frequency_getter.set_user_word_frequency_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return cluster_word_frequency_getter