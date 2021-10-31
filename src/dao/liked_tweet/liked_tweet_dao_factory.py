from src.dao.liked_tweet.getter.mongo_liked_tweet_getter import \
    LikedTweetGetter, MongoLikedTweetGetter
from src.dao.liked_tweet.setter.mongo_liked_tweet_setter import \
    LikedTweetSetter, MongoLikedTweetSetter
from src.shared.mongo import get_collection_from_config
from typing import Dict


class LikedTweetDAOFactory():
    def create_getter(liked_tweets: Dict) -> LikedTweetGetter:
        liked_tweet_getter = None
        if liked_tweets["type"] == "Mongo":
            liked_tweet_getter = MongoLikedTweetGetter()
            collection = get_collection_from_config(liked_tweets["config"])
            liked_tweet_getter.set_tweet_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return liked_tweet_getter

    def create_setter(liked_tweets: Dict) -> LikedTweetSetter:
        liked_tweet_setter = None
        if liked_tweets["type"] == "Mongo":
            liked_tweet_setter = MongoLikedTweetSetter()
            collection = get_collection_from_config(liked_tweets["config"])
            liked_tweet_setter.set_tweet_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return liked_tweet_setter
