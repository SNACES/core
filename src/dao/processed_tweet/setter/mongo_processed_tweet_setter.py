from typing import List, Dict, Set
from src.dao.processed_tweet.setter.processed_tweet_setter import ProcessedTweetSetter
from src.dao.mongo.mongo_dao import MongoDAO
from src.model.processed_tweet import ProcessedTweet
from src.model.tweet import Tweet
import bson


class MongoProcessedTweetSetter(ProcessedTweetSetter, MongoDAO):
    """
    An abstract class representing an object that stores tweets in a
    datastore
    """

    def store_processed_tweet(self, processed_tweet, check=True):
        if check:
            if self._contains_processed_tweet(processed_tweet):
                pass
            else:
                self.collection.insert_one(processed_tweet.toDict())
        else:
            self.collection.insert_one(processed_tweet.toDict())

    def _contains_processed_tweet(self, processed_tweet: ProcessedTweet) -> bool:
        return self.collection.find_one({"id": bson.int64.Int64(processed_tweet.id)}) is not None

    def get_ids_by_user(self, user_id) -> Set[str]:
        tweet_doc_list = self.collection.find({"user_id": bson.int64.Int64(user_id)})

        ids = []
        for doc in tweet_doc_list:
            ids.append(doc.get("user_id"))

        return set(ids)

    def contains_tweet(self, tweet: Tweet) -> bool:
        return self.collection.find_one({"id": bson.int64.Int64(tweet.id)}) is not None
