from typing import List, Dict
from src.model.tweet import Tweet

class RawTweetSetter:
    """
    An abstract class representing an object that stores tweets in a
    datastore
    """

    def store_tweet(self, tweet: Tweet):
        raise NotImplementedError("Subclasses should implement this")

    def store_tweets(self, tweets: List[Tweet]) -> None:
        for tweet in tweets:
            self.store_tweet(tweet)
