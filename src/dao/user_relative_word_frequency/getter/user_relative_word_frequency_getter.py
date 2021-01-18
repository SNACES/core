from typing import List, Dict

class UserRelativeWordFrequencyGetter:
    def get_user_relative_word_frequency_vector(self, user_id: str) -> Dict:
        raise NotImplementedError("Subclasses should implement this")