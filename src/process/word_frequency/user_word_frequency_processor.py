from typing import Union, List
from src.model.word_frequency_vector import WordFrequencyVector
from src.model.user_word_frequency_vector import UserWordFrequencyVector


class UserWordFrequencyProcessor():
    """
    Process and store a users word frequency
    """

    def __init__(self, processed_tweet_getter, user_word_frequency_vector_getter,
            user_word_frequency_vector_setter):
        self.processed_tweet_getter = processed_tweet_getter
        self.user_word_frequency_vector_getter = user_word_frequency_vector_getter
        self.user_word_frequency_vector_setter = user_word_frequency_vector_setter

    def process_user_word_frequency_vector(self, id: str):
        user_processed_tweets = self.processed_tweet_getter.get_user_processed_tweets(id)
        user_word_freq_vc = self.user_word_frequency_vector_getter.get_user_word_frequency_by_id(id).get_word_frequency_vector()

        for processed_tweet in user_processed_tweets:
            user_word_freq_vc += processed_tweet

        self.user_word_frequency_vector_setter.store_user_word_frequency_vector(id, user_word_freq_vc.get_words_dict())


    
