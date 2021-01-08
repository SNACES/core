from typing import List, Dict
import bson
from src.dao.processed_tweet.setter.processed_tweet_setter import ProcessedTweetSetter
from src.dao.mongo.mongo_dao import MongoDAO
from src.model.processed_tweet import ProcessedTweet


class MongoProcessedTweetSetter(ProcessedTweetSetter, MongoDAO):
    """
    An abstract class representing an object that stores tweets in a
    datastore
    """

    def store_processed_tweet(self, processed_tweet):
        if self._contains_processed_tweet(processed_tweet):
            pass
        else:
            self.collection.insert_one(processed_tweet.__dict__)

    def _contains_processed_tweet(self, processed_tweet: ProcessedTweet) -> bool:
        return self.collection.find_one({"id": bson.int64.Int64(processed_tweet.id)}) is not None
