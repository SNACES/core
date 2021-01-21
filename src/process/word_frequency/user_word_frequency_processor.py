from typing import Union, List, Dict
from src.model.word_frequency_vector import WordFrequencyVector
from src.model.user_word_frequency_vector import UserWordFrequencyVector
from copy import deepcopy


class UserWordFrequencyProcessor():
    """
    Process and store a users word frequency
    """

    def __init__(self, processed_tweet_getter, user_word_frequency_vector_getter,
            user_word_frequency_vector_setter, global_word_frequency_vector_getter,
            user_relative_word_frequency_vector_setter):
        self.processed_tweet_getter = processed_tweet_getter
        self.user_word_frequency_vector_getter = user_word_frequency_vector_getter
        self.user_word_frequency_vector_setter = user_word_frequency_vector_setter
        self.global_word_frequency_vector_getter = global_word_frequency_vector_getter
        self.user_relative_word_frequency_vector_setter = user_relative_word_frequency_vector_setter

    def process_user_word_frequency_vector(self, id: str):
        user_processed_tweets = self.processed_tweet_getter.get_user_processed_tweets(id)
        user_word_freq_vc = self.user_word_frequency_vector_getter.get_user_word_frequency_by_id(id).get_word_frequency_vector()

        for processed_tweet in user_processed_tweets:
            user_word_freq_vc += processed_tweet

        self.user_word_frequency_vector_setter.store_user_word_frequency_vector(id, user_word_freq_vc.get_words_dict())
    
    def process_relative_user_word_frequency(self, id: str):
        global_word_count_vc = self.global_word_frequency_vector_getter.get_global_word_frequency()
        user_word_freq_vc = self.user_word_frequency_vector_getter.get_user_word_frequency_by_id(id).get_words()

        relative_user_word_frequency = self._gen_relative_word_frequency(user_word_freq_vc, global_word_count_vc)
        self.user_relative_word_frequency_vector_setter.store_relative_user_word_frequency_vector(id, relative_user_word_frequency)

    def _gen_relative_word_frequency(self, user_word_count, global_word_count):
        merge_count = self._merge_word_count(user_word_count, global_word_count)
        user_word_frequency = self._gen_word_frequency(user_word_count)
        global_word_frequency =self._gen_word_frequency(merge_count)

        for words in user_word_frequency:
            user_word_frequency[words] = user_word_frequency[words] / global_word_frequency[words]
        return user_word_frequency

    def _gen_word_frequency(self, word_counts: Dict):
        word_count = deepcopy(word_counts)
        total_count = sum(word_count.values())
        for words in word_count:
            word_count[words] = word_count[words] / total_count
        return word_count
    
    def _merge_word_count(self, user_word_count, global_word_counts):
        global_word_count = deepcopy(global_word_counts)
        for words in user_word_count:
            if words in global_word_count:
                global_word_count[words] += user_word_count[words]
            else:
                global_word_count[words] = user_word_count[words]
        return global_word_count



    


        


    
