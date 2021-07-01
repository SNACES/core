from typing import List, Dict
import bson
from src.model.tweet import Tweet
from src.shared.utils import get_unique_list
from src.dao.raw_tweet.setter.raw_tweet_setter import RawTweetSetter
from datetime import datetime

class MongoRawTweetSetter(RawTweetSetter):
    """
    An implementation of RawTweetSetter that stores tweet in a MongoDB collection
    """
    def __init__(self):
        self.collection = None

    def set_tweet_collection(self, tweet_collection: str) -> None:
        self.collection = tweet_collection

    def store_tweet(self, tweet):
        if self._contains_tweet(tweet):
            # TODO: decide if this should be an exception
            pass
        else:
            date = tweet.created_at
            if type(date) != datetime:
                proper_date = datetime.strptime(date, '%a %b %d %H:%M:%S +0000 %Y')
                tweet.created_at = proper_date
                # print('updated created_at to datetime\n')
            self.collection.insert_one(tweet.__dict__)

    def _contains_tweet(self, tweet: Tweet) -> bool:
        return self.collection.find_one({"id": bson.int64.Int64(tweet.id)}) is not None

    def get_num_user_tweets(self, user_id) -> int:
        return self.collection.count({"user_id": bson.int64.Int64(user_id)})

    def get_num_tweets(self) -> int:
        """
        Returns the number of tweets in the mongo collection

        @return the number of tweets
        """
        # We call count with a blank query {} so that it returns an accurate
        # result, rather than relying on the metadata which gives an approximate
        # result. However this is slower
        return self.collection.count({})
