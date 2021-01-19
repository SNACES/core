from typing import List, Dict

class GlobalWordFrequencySetter:
    """
    An abstract class representing an object that stores global word frequency vector in a datastore
    """

    def store_global_word_frequency_vector(self, global_word_freq_vc: Dict):
        raise NotImplementedError("Subclasses should implement this")