from src.dao.user_relative_word_frequency.setter.user_relative_word_frequency_setter import UserRelativeWordFrequencySetter
from src.dao.user_relative_word_frequency.setter.mongo_user_relative_word_frequency_setter import MongoUserRelativeWordFrequencySetter
from src.dao.user_relative_word_frequency.getter.user_relative_word_frequency_getter import UserRelativeWordFrequencyGetter
from src.dao.user_relative_word_frequency.getter.mongo_user_relative_word_frequency_getter import MongoUserRelativeWordFrequencyGetter
from src.shared.mongo import get_collection_from_config
from typing import Dict

class UserRelativeWordFrequencyDAOFactory():
    def create_setter(config: Dict) -> UserRelativeWordFrequencySetter:
        user_relative_word_frequency_setter = None
        if config["type"] == "Mongo":
            user_relative_word_frequency_setter = MongoUserRelativeWordFrequencySetter()
            collection = get_collection_from_config(config["config"])
            user_relative_word_frequency_setter.set_user_relative_word_frequency_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return user_relative_word_frequency_setter

    def create_getter(config: Dict) -> UserRelativeWordFrequencyGetter:
        user_relative_word_frequency_getter = None
        if config["type"] == "Mongo":
            user_relative_word_frequency_getter = MongoUserRelativeWordFrequencyGetter()
            collection = get_collection_from_config(config["config"])
            user_relative_word_frequency_getter.set_user_relative_word_frequency_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return user_relative_word_frequency_getter
