from typing import List, Dict
import bson
from src.model.user_word_frequency_vector import UserWordFrequencyVector
from src.model.word_frequency_vector import WordFrequencyVector
from src.dao.user_relative_word_frequency.getter.user_relative_word_frequency_getter import UserRelativeWordFrequencyGetter


class MongoUserRelativeWordFrequencyGetter(UserRelativeWordFrequencyGetter):
    def __init__(self):
        self.user_relative_word_frequency_collection = None

    def set_user_relative_word_frequency_collection(self, user_relative_word_frequency_collection: str) -> None:
        self.user_relative_word_frequency_collection = user_relative_word_frequency_collection
    
    def get_user_relative_word_frequency_by_id(self, user_id: str) -> UserWordFrequencyVector:
        doc = self.user_relative_word_frequency_collection.find_one({"user_id": bson.int64.Int64(user_id)})
        if doc is not None:
            return doc["relative_word_frequency_vector"]
        else:
            return None