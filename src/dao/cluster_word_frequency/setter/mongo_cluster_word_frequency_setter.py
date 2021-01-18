from typing import List, Dict
from src.model.cluster_word_frequency_vector import ClusterWordFrequencyVector
from src.dao.cluster_word_frequency.setter import ClusterWordFrequencySetter

class MongoClusterWordFrequencyerSetter(ClusterWordFrequencySetter):
    def __init__(self):
        self.cluster_word_frequency_collection = None

    def set_cluster_word_frequency_collection(self, cluster_word_frequency_collection: str) -> None:
        self.cluster_word_frequency_collection = cluster_word_frequency_collection

    def store_cluster_word_frequency_vector(self, user_ids: List[str], user_word_freq_vc: Dict):
        doc = { "user_ids": user_ids, "word_count": sum(user_word_freq_vc.keys()),"word_frequency_vector": user_word_freq_vc}

        if self._contains_user(user_ids):
            self.user_word_frequency_collection.find_one_and_replace({"user_ids": user_ids}, doc)
        else:
            self.user_word_frequency_collection.insert_one(doc)

    def _contains_user(self, user_ids) -> bool:
        return self.user_word_frequency_collection.find_one({"user_ids": user_ids}) is not None



    