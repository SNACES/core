from src.dao.raw_tweet.setter.raw_tweet_setter import RawTweetSetter
from src.dao.raw_tweet.setter.mongo_raw_tweet_setter import MongoRawTweetSetter
from src.dao.raw_tweet.getter.raw_tweet_getter import RawTweetGetter
from src.dao.raw_tweet.getter.mongo_raw_tweet_getter import MongoRawTweetGetter
from src.shared.mongo import get_collection_from_config
from typing import Dict

class RawTweetDAOFactory():
    def create_getter(raw_tweets: Dict) -> RawTweetGetter:
        raw_tweet_better = None
        if raw_tweets["type"] == "Mongo":
            raw_tweet_better = MongoRawTweetGetter()
            collection = get_collection_from_config(raw_tweets["config"])
            raw_tweet_getter.set_tweet_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return raw_tweet_getter

    def create_setter(raw_tweets: Dict) -> RawTweetSetter:
        raw_tweet_setter = None
        if raw_tweets["type"] == "Mongo":
            raw_tweet_setter = MongoRawTweetSetter()
            collection = get_collection_from_config(raw_tweets["config"])
            raw_tweet_setter.set_tweet_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return raw_tweet_setter
