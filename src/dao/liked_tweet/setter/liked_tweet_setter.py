from typing import List

from src.model.liked_tweet import LikedTweet

class LikedTweetSetter:
    """
    An abstract class representing an object that stores tweets in a
    datastore
    """
    def store_tweet(self, tweet: LikedTweet):
        raise NotImplementedError("Subclasses should implement this")

    def store_tweets(self, tweets: List[LikedTweet]) -> None:
        for tweet in tweets:
            self.store_tweet(tweet)
