from typing import Dict
from src.dao.twitter.twitter_dao_factory import TwitterDAOFactory
from src.dao.raw_tweet.raw_tweet_dao_factory import RawTweetDAOFactory
from src.process.download.tweet_downloader import TwitterTweetDownloader


class DownloadTweetsActivity():
    def __init__(self, config: Dict):
        self.tweet_downloader = None
        self.configure(config)

    def configure(self, config: Dict):
        if config is not None:
            # Configure input datastore
            input_datastore = config["input-datastore"]
            download_source = input_datastore["Download-Source"]

            twitter_getter = TwitterDAOFactory.create_getter(download_source)

            # Configure output datastore
            output_datastore = config["output-datastore"]
            raw_tweets = output_datastore["RawTweets"]

            raw_tweet_setter = RawTweetDAOFactory.create_getter(raw_tweets)

            self.tweet_downloader = TwitterTweetDownloader(
                twitter_getter,
                raw_tweet_setter)

    def stream_random_tweets(self, num_tweets):
        self.tweet_downloader.stream_random_tweets(num_tweets=num_tweets)
