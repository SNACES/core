import time
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

    def stream_random_tweets(self, num_tweets=1) -> None:
        before = self.raw_tweet_setter.get_num_tweets()
        subscriber = self.Subscriber(self.raw_tweet_setter)
        try:
            self.tweepy_getter.buffered_stream_tweets(
                num_tweets=num_tweets,
                subscriber=subscriber)
        except Exception as e:
            after = self.raw_tweet_setter.get_num_tweets()
            print("Stored only %d tweets" %(after - before))
            raise e

        after = self.raw_tweet_setter.get_num_tweets()
        print("Stored %d tweets" %(after - before))

    class Subscriber():
        def __init__(self, raw_tweet_setter: RawTweetSetter):
            self.raw_tweet_setter = raw_tweet_setter

        def on_status(self, data):
            tweet = Tweet.fromTweepyJSON(data._json)
            self.raw_tweet_setter.store_tweet(tweet)
