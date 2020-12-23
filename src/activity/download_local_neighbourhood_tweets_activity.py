from src.dao.twitter.twitter_dao_factory import TwitterDAOFactory
# from src.dao.user_friend.user_friend_dao_factory import UserFriendDAOFactory
from src.dao.local_neighbourhood.local_neighbourhood_dao_factory import LocalNeighbourhoodDAOFactory
# from src.dao.user.user_dao_factory import UserDAOFactory
from src.dao.raw_tweet.raw_tweet_dao_factory import RawTweetDAOFactory
from src.process.download.user_tweet_downloader import UserTweetDownloader
# from src.process.download.friend_downloader import FriendDownloader
from src.process.download.local_neighbourhood_tweet_downloader import LocalNeighbourhoodTweetDownloader
from typing import Dict


class DownloadLocalNeighbourhoodTweetsActivity():
    """
    Given an user, download their local neighbourhood
    """

    def __init__(self, config: Dict):
        self.local_neighbourhood_tweet_downloader = None

        self.configure(config)

    def configure(self, config: Dict):
        if config is not None:
            # Configure input datastore
            input_datastore = config["input-datastore"]
            download_source = input_datastore["Download-Source"]
            local_neighbourhood = input_datastore["LocalNeighbourhoods"]

            twitter_getter = TwitterDAOFactory.create_getter(download_source)
            local_neighbourhood_getter = LocalNeighbourhoodDAOFactory.create_getter(local_neighbourhood)

            # Configure output datastore
            output_datastore = config["output-datastore"]
            user_tweets = output_datastore["UserTweets"]

            raw_tweet_setter = RawTweetDAOFactory.create_setter(user_tweets)

            user_tweet_downloader = UserTweetDownloader(
                twitter_getter,
                raw_tweet_setter)

            self.local_neighbourhood_tweet_downloader = LocalNeighbourhoodTweetDownloader(user_tweet_downloader, local_neighbourhood_getter)

    def download_local_neighbourhood_tweets_by_user_id(self, user_id: str, params=None):
        self.local_neighbourhood_tweet_downloader.download_user_tweets_by_local_neighbourhood(user_id, params)
