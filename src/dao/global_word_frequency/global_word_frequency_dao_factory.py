from src.dao.global_word_frequency.setter.global_word_frequency_setter import GlobalWordFrequencySetter
from src.dao.global_word_frequency.setter.mongo_global_word_frequency_setter import MongoGlobalWordFrequencySetter
from src.dao.global_word_frequency.getter.global_word_frequency_getter import GlobalWordFrequencyGetter
from src.dao.global_word_frequency.getter.mongo_global_word_frequency_getter import MongoGlobalWordFrequencyGetter
from src.shared.mongo import get_collection_from_config
from typing import Dict

class GlobalWordFrequencyDAOFactory():
    def create_setter(config: Dict) -> GlobalWordFrequencySetter:
        global_word_frequency_setter = None
        if config["type"] == "Mongo":
            global_word_frequency_setter = MongoGlobalWordFrequencySetter()
            collection = get_collection_from_config(config["config"])
            global_word_frequency_setter.set_global_word_frequency_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return global_word_frequency_setter

    def create_getter(config: Dict) -> GlobalWordFrequencyGetter:
        global_word_frequency_getter = None
        if config["type"] == "Mongo":
            global_word_frequency_getter = MongoGlobalWordFrequencyGetter()
            collection = get_collection_from_config(config["config"])
            global_word_frequency_getter.set_global_word_frequency_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return global_word_frequency_getter
