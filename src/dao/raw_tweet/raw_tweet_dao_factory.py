from src.dao.raw_tweet.setter.raw_tweet_setter import RawTweetSetter
from src.dao.raw_tweet.setter.mongo_raw_tweet_setter import MongoRawTweetSetter
from src.shared.mongo import get_collection_from_config
from typing import Dict

class RawTweetDAOFactory():
    def create_getter(raw_tweets: Dict) -> RawTweetSetter:
        raw_tweet_setter = None
        if raw_tweets["type"] == "Mongo":
            raw_tweet_setter = MongoRawTweetSetter()
            collection = get_collection_from_config(raw_tweets["config"])
            raw_tweet_setter.set_tweet_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return raw_tweet_setter
