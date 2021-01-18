from src.dao.cluster_relative_word_frequency.setter.cluster_relative_word_frequency_setter import ClusterRelativeWordFrequencySetter
from src.dao.cluster_relative_word_frequency.setter.mongo_cluster_relative_word_frequency_setter import MongoClusterRelativeWordFrequencySetter
from src.dao.cluster_relative_word_frequency.getter.cluster_relative_word_frequency_getter import ClusterRelativeWordFrequencyGetter
from src.dao.cluster_relative_word_frequency.getter.mongo_cluster_relative_word_frequency_getter import MongoClusterRelativeWordFrequencyGetter
from src.shared.mongo import get_collection_from_config
from typing import Dict

class ClusterWordFrequencyDAOFactory():
    def create_setter(config: Dict) -> ClusterRelativeWordFrequencySetter:
        cluster_relative_word_frequency_setter = None
        if config["type"] == "Mongo":
            cluster_relative_word_frequency_setter = MongoClusterRelativeWordFrequencySetter()
            collection = get_collection_from_config(config["config"])
            cluster_relative_word_frequency_setter.set_cluster_relative_word_frequency_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return cluster_relative_word_frequency_setter

    def create_getter(config: Dict) -> ClusterRelativeWordFrequencyGetter:
        cluster_relative_word_frequency_getter = None
        if config["type"] == "Mongo":
            cluster_relative_word_frequency_getter = MongoClusterRelativeWordFrequencyGetter()
            collection = get_collection_from_config(config["config"])
            cluster_relative_word_frequency_getter.set_cluster_relative_word_frequency_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return cluster_relative_word_frequency_getter