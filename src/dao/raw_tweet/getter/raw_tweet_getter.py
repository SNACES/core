from typing import List, Dict
from src.model.tweet import Tweet
from src.model.user import User


class RawTweetGetter:
    """
    An abstract class representing an object that reads tweets in from a
    datastore
    """

    def get_tweet_by_id(self) -> List[Tweet]:
        raise NotImplementedError("Subclasses should implement this")

    def get_tweets_by_user(self, user: User) -> Dict[str, List[Tweet]]:
        raise NotImplementedError("Subclasses should implement this")

    def get_tweets_by_user_id(self, user, start_date, end_date, get_retweets=False):
        raise NotImplementedError("Subclasses should implement this")

    def get_num_tweets(self):
        raise NotImplementedError("Subclasses should implement this")
