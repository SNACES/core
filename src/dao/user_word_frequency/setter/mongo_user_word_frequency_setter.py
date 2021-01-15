from typing import List, Dict
from src.model.user_word_frequency_vector import UserWordFrequencyVector
from src.dao.user_word_frequency.setter import UserWordFrequencySetter

class MongoUserWordFrequencyerSetter(UserWordFrequencySetter):
    def __init__(self):
        self.user_word_frequency_collection = None
        self.relative_user_word_frequency_collection = None

    def set_user_word_frequency_collection(self, user_word_frequency_collection: str) -> None:
        self.user_word_frequency_collection = user_word_frequency_collection

    def set_relative_user_word_frequency_collection(self, relative_user_word_frequency_collection: str) -> None:
        self.relative_user_word_frequency_collection = relative_user_word_frequency_collection

    def store_user_word_frequency_vector(self, user_id:str, user_word_freq_vc: Dict):
        doc = { "user_id": user_id, "word_count": sum(user_word_freq_vc.keys()),"word_frequency_vector": user_word_freq_vc}

        if self._contains_user(user_id):
            self.user_word_frequency_collection.find_one_and_replace({"user_id": user_id}, doc)
        else:
            self.user_word_frequency_collection.insert_one(doc)

    def store_relative_user_word_frequency_vector(self, user_id:str, relative_user_word_freq_vc: Dict):
        doc = { "user_id": user_id, "relative_word_frequency_vector": relative_user_word_freq_vc}

        if self._contains_user_relative(user_id):
            self.relative_user_word_frequency_collection.find_one_and_replace({"user_id": user_id}, doc)
        else:
            self.relative_user_word_frequency_collection.insert_one(doc) 

    def _contains_user(self, user_id) -> bool:
        return self.user_word_frequency_collection.find_one({"user_id": user_id}) is not None

    def _contains_user_relative(self, user_id) -> bool:
        return self.relative_user_word_frequency_collection.find_one({"user_id": user_id}) is not None

    