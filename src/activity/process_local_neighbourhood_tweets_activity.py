from typing import Dict
from src.shared.mongo import get_collection_from_config
from src.dao.raw_tweet.getter.mongo_raw_tweet_getter import MongoRawTweetGetter
from src.dao.processed_tweet.setter.mongo_processed_tweet_setter import MongoProcessedTweetSetter
from src.process.raw_tweet_processing.tweet_processor import TweetProcessor
from src.dao.raw_tweet.raw_tweet_dao_factory import RawTweetDAOFactory
from src.dao.local_neighbourhood.local_neighbourhood_dao_factory import LocalNeighbourhoodDAOFactory
from src.dao.processed_tweet.processed_tweet_dao_factory import ProcessedTweetDAOFactory


class ProcessLocalNeighbourhoodTweetsActivity():
    def __init__(self, config: Dict):
        self.tweet_processor = None
        self.local_neighbourhood_getter = None

        self.configure(config)

    def configure(self, config: Dict):
        if config is not None:
            input_datastore = config["input-datastore"]

            raw_tweet = input_datastore['UserTweet']
            local_neighbourhood = input_datastore['LocalNeighbourhood']

            raw_tweet_getter = RawTweetDAOFactory.create_getter(raw_tweet)
            local_neighbourhood_getter = LocalNeighbourhoodDAOFactory.create_getter(local_neighbourhood)

            output_datastore = config["output-datastore"]

            processed_tweet = output_datastore['ProcessedTweet']

            processed_tweet_setter = ProcessedTweetDAOFactory.create_setter(processed_tweet)

            self.tweet_processor = TweetProcessor(raw_tweet_getter,
                processed_tweet_setter)

            self.local_neighbourhood_getter = local_neighbourhood_getter

    def process_local_neighbourhood_tweets(self, seed_id: str, params=None):
        local_neighbourhood = self.local_neighbourhood_getter.get_local_neighbourhood(seed_id, params)
        self.tweet_processor.process_tweets_by_local_neighbourhood(local_neighbourhood)
