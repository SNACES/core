from src.shared.mongo import get_collection_from_config
from src.dao.twitter.tweepy_twitter_dao import TweepyTwitterGetter
from src.dao.raw_tweet.setter.mongo_raw_tweet_setter import MongoRawTweetSetter
from src.process.download.tweet_downloader import TwitterTweetDownloader
from typing import Dict

class DownloadTweetsActivity():
    def __init__(self, config: Dict):
        self.tweet_downloader = None
        self.configure(config)

    def configure(self, config: Dict):
        if config is not None:
            tweepy_getter = TweepyTwitterGetter()
            raw_tweet_setter = MongoRawTweetSetter()

            collection = get_collection_from_config(config)

            raw_tweet_setter.set_tweet_collection(collection)

            self.tweet_downloader = TwitterTweetDownloader(
                tweepy_getter,
                raw_tweet_setter)

    def stream_random_tweets(self, num_tweets):
        self.tweet_downloader.stream_random_tweets(num_tweets=num_tweets)
