import functools
import datetime
from typing import Union, List
from src.model.tweet import Tweet
from src.dao.twitter.tweepy_twitter_dao import TweepyTwitterGetter
from src.dao.raw_tweet.setter.raw_tweet_setter import RawTweetSetter

class TwitterTweetDownloader():
    """
    Downloads a twitter tweet downloader 
    """

    def __init__(self, tweepy_getter: TweepyTwitterGetter, raw_tweet_setter: RawTweetSetter):
        self.tweepy_getter = tweepy_getter
        self.raw_tweet_setter = raw_tweet_setter

    def download_random_tweet(self) -> None:
        """
        Retrieves a random tweet from Twitter, and stores it in using its
        tweet dao
        """
        tweet = self.tweepy_getter.get_random_tweet()
        self.raw_tweet_setter.store_tweet(tweet)
