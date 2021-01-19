from src.dao.user_word_frequency.setter.user_word_frequency_setter import UserWordFrequencySetter
from src.dao.user_word_frequency.setter.mongo_user_word_frequency_setter import MongoUserWordFrequencySetter
from src.dao.user_word_frequency.getter.user_word_frequency_getter import UserWordFrequencyGetter
from src.dao.user_word_frequency.getter.mongo_user_word_frequency_getter import MongoUserWordFrequencyGetter
from src.shared.mongo import get_collection_from_config
from typing import Dict

class UserWordFrequencyDAOFactory():
    def create_setter(config: Dict) -> UserWordFrequencySetter:
        user_word_frequency_setter = None
        if config["type"] == "Mongo":
            user_word_frequency_setter = MongoUserWordFrequencySetter()
            collection = get_collection_from_config(config["config"])
            user_word_frequency_setter.set_user_word_frequency_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return user_word_frequency_setter

    def create_getter(config: Dict) -> UserWordFrequencyGetter:
        user_word_frequency_getter = None
        if config["type"] == "Mongo":
            user_word_frequency_getter = MongoUserWordFrequencyGetter()
            collection = get_collection_from_config(config["config"])
            user_word_frequency_getter.set_user_word_frequency_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return user_word_frequency_getter
