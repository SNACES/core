from src.dao.global_word_frequency.global_word_frequency_dao_factory import GlobalWordFrequencyDAOFactory
from src.dao.processed_tweet.processed_tweet_dao_factory import ProcessedTweetDAOFactory
from src.dao.user_relative_word_frequency.user_relative_word_frequency_dao_factory import UserRelativeWordFrequencyDAOFactory
from src.dao.user_word_frequency.user_word_frequency_dao_factory import UserWordFrequencyDAOFactory
from src.process.word_frequency.user_word_frequency_processor import UserWordFrequencyProcessor
from typing import Dict


class UserWordFrequencyActivity():
    """
    """

    def __init__(self, config: Dict):
        self.user_word_frequency = None

        self.configure(config)

    def configure(self, config: Dict):
        if config is not None:
            # Configure input datastore
            input_datastore = config["input-datastore"]

            processed_tweets = input_datastore["ProcessedTweet"]
            user_word_frequency = input_datastore["UserWordFrequency"]
            global_word_frequency = input_datastore["GlobalWordFrequency"]

            processed_tweets_getter = ProcessedTweetDAOFactory.create_getter(processed_tweets)
            user_word_frequency_getter = UserWordFrequencyDAOFactory.create_getter(user_word_frequency)
            global_word_frequency_getter = GlobalWordFrequencyDAOFactory.create_getter(global_word_frequency)


            # Configure output datastore
            output_datastore = config["output-datastore"]

            user_word_frequency_out = output_datastore["UserWordFrequency"]
            relative_user_word_frequency_out = output_datastore["RelativeUserWordFrequency"]

            user_word_frequency_setter = UserWordFrequencyDAOFactory.create_setter(user_word_frequency_out)
            relative_user_word_frequency_setter = UserRelativeWordFrequencyDAOFactory.create_setter(relative_user_word_frequency_out)

            self.user_word_frequency = UserWordFrequencyProcessor(processed_tweets_getter, user_word_frequency_getter,
                                            user_word_frequency_setter, global_word_frequency_getter,
                                            relative_user_word_frequency_setter)

    def get_user_word_frequency(self, seed_id):
        self.user_word_frequency.process_user_word_frequency_vector(seed_id)
        self.user_word_frequency.process_relative_user_word_frequency(seed_id)