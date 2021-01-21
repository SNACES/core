from copy import deepcopy
from typing import Dict
from src.model.word_frequency_vector import WordFrequencyVector
from copy import deepcopy


class UserWordFrequencyVector():
    def __init__(self, id: str, word_frequency_vector: Dict):
        """
        Format is as follows:
        e.g. {
            user_id: 100001, 
            word_frequency_vector: {
                "hello": 2,
                "goodbye": 3
             }
             }
        """
        self.id = id
        self.word_frequency_vector = WordFrequencyVector.fromDict(word_frequency_vector)
        self.words = word_frequency_vector
        self.total_count = sum(word_frequency_vector.values())

    def __add__(self, other):

        v1 = self.words.deepcopy()
        v2 = other.words.deepcopy()

        v = WordFrequencyVector.fromDict(v1) + WordFrequencyVector.fromDict(v2)
        result = {"user_id": id, "word_frequency_vector":v.get_words_dict()}

        return UserWordFrequencyVector.fromDict(result)

    def fromDict(dict: Dict):
        user_wf_vector = UserWordFrequencyVector(dict["user_id"], dict["word_frequency_vector"])

        return user_wf_vector

    def set_total_count(self, word_count: int):
        self.total_count = word_count

    def get_total_count(self):
        return self.total_count

    def get_word_frequency_vector(self):
        return self.word_frequency_vector

    def get_words(self):
        return self.words
