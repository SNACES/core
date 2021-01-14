from copy import deepcopy
from typing import Dict


class WordFrequencyVector():
    def __init__(self, words: Dict):
        """
        Words is a dictionary representing a word frequency vector
        e.g. {
                "hello": 2,
                "goodbye": 3
             }
        """
        self.words = words

    def __add__(self, other):
        v1 = self.words
        v2 = other.words

        result = deepcopy(v1)
        for word in v2.keys():
            if word in v2:
                result[word] += v2[word]
            else:
                result[word] = v2[word]

        return result

    def fromDict(dict: Dict):
        wf_vector = WordFrequencyVector(dict)

        return wf_vector
