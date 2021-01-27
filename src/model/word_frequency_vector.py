from copy import deepcopy
from typing import Dict


class WordFrequencyVector():
    def __init__(self, words: Dict[str, int]):
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
            if word in result:
                result[word] += v2[word]
            else:
                result[word] = v2[word]

        return WordFrequencyVector.fromDict(result)

    def fromDict(dict: Dict):
        wf_vector = WordFrequencyVector(dict)

        return wf_vector

    def cosine_sim_to(self, other) -> float:
        """
        An implementation of cosine similarity based on word counters rather than vectors

        @param self The first word vector to compare
        @param other The second word vector to compare
        """
        counter1 = self.words
        counter2 = other.words

        norm_c1 = sum([x**2 for x in counter1.values()])**0.5
        norm_c2 = sum([x**2 for x in counter2.values()])**0.5
        dot_product = 0
        for key in set.intersection(set(counter1.keys()), set(counter2.keys())):
            dot_product += counter1[key]*counter2[key]

        return dot_product/(norm_c1*norm_c2) if norm_c1 != 0 and norm_c2 != 0 else -1

    def get_words_dict(self):
        return self.words
