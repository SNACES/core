import bson
from typing import Dict
from src.shared.mongo import get_collection_from_config

class MongoLikedTweetIndicator():
    """
    Implementation of LikedTweetIndicator that indicates if we have stored
    a user's liked tweet from MongoDB
    """

    def __init__(self, liked_tweets_indicator: Dict):
        self.collection = get_collection_from_config(liked_tweets_indicator["config"])

    def contains_user(self, user_id: str) -> bool:
        """
        Return tweet with id that matches the given id

        @param id the id of the tweet to get

        @return the Tweet object corresponding to the tweet id, or none if no
            tweet matches the given id
        """
        tweet_doc = self.collection.find_one({"user_id": bson.int64.Int64(user_id)})
        if tweet_doc is not None:
            return True
        else:
            return False

    def store_user(self, user_id):
        self.collection.insert_one({"user_id": bson.int64.Int64(user_id)})
