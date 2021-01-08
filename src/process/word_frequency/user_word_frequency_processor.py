from typing import Union, List
from src.model.word_frequency_vector import WordFrequencyVector


class UserWordFrequencyProcessor():
    """
    """

    def __init__(self, processed_tweet_getter, word_frequency_vector_getter,
            user_word_frequency_vector_setter):
        self.processed_tweet_getter = processed_tweet_getter
        self.word_frequency_vector_getter = word_frequency_vector_getter
        self.word_frequency_vector_setter = word_frequency_vector_setter

    def process_user_word_frequency_vector(id: str):
        user_processed_tweets = self.processed_tweet_getter.get_user_processed_tweets(id)

        word_frequency_vector = WordFrequencyVector(id)
        for processed_tweet in user_processed_tweets:
            word_frequency_vector.add_processed_tweet(processed_tweet)

        word_frequency_vector_setter.store_user_word_frequency_vector()
        print(word_frequency_vector)
