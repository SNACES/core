from typing import Dict
from src.shared.mongo import get_collection_from_config
from src.dao.raw_tweet.getter.mongo_raw_tweet_getter import MongoRawTweetGetter
from src.dao.processed_tweet.setter.mongo_processed_tweet_setter import MongoProcessedTweetSetter
from src.process.raw_tweet_processing.tweet_processor import TweetProcessor


class ProcessTweetActivity():
    def __init__(self, config: Dict):
        self.tweet_processor = None
        self.configure(config)

    def configure(self, config: Dict):
        if config is not None:
            raw_tweet_getter = MongoRawTweetGetter()
            processed_tweet_setter = MongoProcessedTweetSetter()

            raw_tweet_config = config['raw_tweets']

            raw_tweets_collection = get_collection_from_config(raw_tweet_config)
            raw_tweet_getter.set_tweet_collection(raw_tweets_collection)

            processed_tweets_config = config['processed_tweets']

            processed_tweets_collection = get_collection_from_config(processed_tweets_config)
            processed_tweet_setter.set_processed_tweet_collection(processed_tweets_collection)

            self.tweet_processor = TweetProcessor(raw_tweet_getter,
                processed_tweet_setter)

    def process_tweet_by_id(self, id: str):
        self.tweet_processor.process_tweet_by_id(id)
