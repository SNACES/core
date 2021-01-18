from typing import List, Dict
from src.model.user_word_frequency_vector import UserWordFrequencyVector

class UserRelativeWordFrequencySetter:
    """
    An abstract class representing an object that stores a users word frequency vector in a datastore
    """

    def store_user_relative_word_frequency_vector(self, user_id:str, user_relative_word_freq_vc: Dict):
        raise NotImplementedError("Subclasses should implement this")