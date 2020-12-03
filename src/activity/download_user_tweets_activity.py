from typing import Dict
from src.shared.mongo import get_collection_from_config
from src.dao.twitter.twitter_dao_factory import TwitterDAOFactory
from src.dao.raw_tweet.raw_tweet_dao_factory import RawTweetDAOFactory
from src.process.download.user_tweet_downloader import UserTweetDownloader

class DownloadUserTweetsActivity():
    def __init__(self, config: Dict):
        self.user_tweet_downloader = None
        self.configure(config)

    def configure(self, config: Dict):
        if config is not None:
            # Configure input datastore
            input_datastore = config["input-datastore"]
            download_source = input_datastore["Download-Source"]

            twitter_getter = TwitterDAOFactory.create_getter(download_source)

            # Configure output datastore
            output_datastore = config["output-datastore"]
            user_tweets = output_datastore["UserTweets"]

            raw_tweet_setter = RawTweetDAOFactory.create_setter(user_tweets)

            self.user_tweet_downloader = UserTweetDownloader(
                twitter_getter,
                raw_tweet_setter)

    def download_user_tweets_by_user_id(self, user_id: str):
        self.user_tweet_downloader.download_user_tweets_by_user_id(user_id)

    def download_user_tweets_by_screen_name(self, screen_name: str):
        self.user_tweet_downloader.download_user_tweets_by_screen_name(screen_name)
