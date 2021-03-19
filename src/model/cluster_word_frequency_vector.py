from copy import deepcopy
from typing import Dict, List
from src.model.word_frequency_vector import WordFrequencyVector
from copy import deepcopy


class ClusterWordFrequencyVector():
    def __init__(self, ids: List[str], word_frequency_vector: Dict):
        """
        Format is as follows:
        e.g. {
            user_ids: [100001, 20003, 458429]
            word_frequency_vector: {
                "hello": 2,
                "goodbye": 3
            }
          }
        """
        self.ids = ids
        self.word_frequency_vector = WordFrequencyVector.fromDict(word_frequency_vector)
        self.words = word_frequency_vector
        self.total_count = sum(word_frequency_vector.values())

    def fromDict(dict: Dict):
        cluster_wf_vector = ClusterWordFrequencyVector(dict["user_ids"], dict["word_frequency_vector"])

        return cluster_wf_vector

    def set_total_count(self, word_count: int):
        self.total_count = word_count

    def get_total_count(self):
        return self.total_count

    def get_word_frequency_vector(self):
        return self.word_frequency_vector

    def get_words(self):
        return self.words
