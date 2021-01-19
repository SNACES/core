from typing import List, Dict
import bson
from src.dao.global_word_frequency.getter.global_word_frequency_getter import GlobalWordFrequencyGetter


class MongoGlobalWordFrequencyGetter(GlobalWordFrequencyGetter):
    def __init__(self):
        self.global_word_frequency_collection = None

    def set_global_word_frequency_collection(self, global_word_frequency_collection: str) -> None:
        self.global_word_frequency_collection = global_word_frequency_collection

    def get_global_word_frequency(self) -> Dict:
        doc = self.global_word_frequency_collection.find()
        if doc is not None:
            return doc["global_word_frequency_vector"]
        else:
            return None