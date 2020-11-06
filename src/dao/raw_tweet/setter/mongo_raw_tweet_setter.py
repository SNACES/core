from typing import List, Dict
from src.model.tweet import Tweet
from src.shared.utils import get_unique_list
from src.dao.raw_tweet.setter.raw_tweet_setter import RawTweetSetter

class MongoRawTweetSetter(RawTweetSetter):
    """
    An implementation of RawTweetSetter that stores tweet in a MongoDB collection
    """
    def __init__(self):
        self.tweet_collection = None

    def set_tweet_collection(self, tweet_collection: str) -> None:
        self.tweet_collection = tweet_collection

    def store_tweets(self, tweets: List[Tweet]) -> None:
        for tweet in tweets:
            self.store_tweet(tweet)

    def store_tweet(self, tweet):
        if self._contains_tweet(tweet):
            # TODO: decide if this should be an exception
            pass
        else:
            self.tweet_collection.insert_one(tweet.__dict__)

    def _contains_tweet(self, tweet: Tweet) -> bool:
        return self.tweet_collection.find_one({"id": tweet.id}) is not None
