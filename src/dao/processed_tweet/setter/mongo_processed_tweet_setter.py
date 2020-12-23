from typing import List, Dict
import bson
from src.dao.processed_tweet.setter.processed_tweet_setter import ProcessedTweetSetter
from src.model.processed_tweet import ProcessedTweet

class MongoProcessedTweetSetter(ProcessedTweetSetter):
    """
    An abstract class representing an object that stores tweets in a
    datastore
    """
    def __init__(self):
        self.processed_tweet_collection = None

    def set_processed_tweet_collection(self, processed_tweet_collection: str) -> None:
        self.processed_tweet_collection = processed_tweet_collection

    def store_processed_tweet(self, processed_tweet):
        if self._contains_processed_tweet(processed_tweet):
            # TODO: decide if this should be an exception
            pass
        else:
            self.processed_tweet_collection.insert_one(processed_tweet.__dict__)

    def _contains_processed_tweet(self, processed_tweet: ProcessedTweet) -> bool:
        return self.processed_tweet_collection.find_one({"id": bson.int64.Int64(processed_tweet.id)}) is not None
