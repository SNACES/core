from typing import Dict
from src.shared.mongo import get_collection_from_config
from src.dao.twitter.tweepy_twitter_dao import TweepyTwitterGetter
from src.dao.raw_tweet.setter.mongo_raw_tweet_setter import MongoRawTweetSetter
from src.process.download.user_tweet_downloader import UserTweetDownloader

class DownloadUserTweetsActivity():
    def __init__(self, config: Dict):
        self.user_tweet_downloader = None
        self.configure(config)

    def configure(self, config: Dict):
        if config is not None:
            tweepy_getter = TweepyTwitterGetter()
            raw_tweet_setter = MongoRawTweetSetter()

            collection = get_collection_from_config(config)

            raw_tweet_setter.set_tweet_collection(collection)

            self.user_tweet_downloader = UserTweetDownloader(
                tweepy_getter,
                raw_tweet_setter)

    def download_user_tweets_by_user_id(self, user_id: str):
        self.user_tweet_downloader.download_user_tweets_by_user_id(user_id)

    def download_user_tweets_by_screen_name(self, screen_name: str):
        self.user_tweet_downloader.download_user_tweets_by_screen_name(screen_name)
