from typing import List, Dict

from src.model.liked_tweet import LikedTweet
from src.model.user import User


class LikedTweetGetter:
    """
    An abstract class representing an object that reads tweets in from a
    datastore
    """

    def get_tweet_by_id(self, user_id: str) -> List[LikedTweet]:
        raise NotImplementedError("Subclasses should implement this")

    def get_tweets_by_user(self, user: User) -> Dict[str, List[LikedTweet]]:
        raise NotImplementedError("Subclasses should implement this")

    def get_tweets_by_user_id(self, user_id: str):
        raise NotImplementedError("Subclasses should implement this")

    def get_num_tweets(self):
        raise NotImplementedError("Subclasses should implement this")
