from src.dao.twitter.twitter_dao_factory import TwitterDAOFactory
from src.dao.user_friend.user_friend_dao_factory import UserFriendDAOFactory
from src.dao.local_neighbourhood.local_neighbourhood_dao_factory import LocalNeighbourhoodDAOFactory
from src.dao.user.user_dao_factory import UserDAOFactory
from src.process.download.user_downloader import TwitterUserDownloader
from src.process.download.friend_downloader import FriendDownloader
from src.process.download.local_neighbourhood_downloader import LocalNeighbourhoodDownloader
from typing import Dict


class DownloadLocalNeighbourhoodActivity():
    """
    Given an user, download their local neighbourhood
    """

    def __init__(self, config: Dict):
        self.local_neighbourhood_downloader = None

        self.configure(config)

    def configure(self, config: Dict):
        if config is not None:
            # Configure input datastore
            input_datastore = config["input-datastore"]
            download_source = input_datastore["Download-Source"]

            twitter_getter = TwitterDAOFactory.create_getter(download_source)

            # Configure output datastore
            output_datastore = config["output-datastore"]
            local_neighbourhood = output_datastore["LocalNeighbourhoods"]

            local_neighbourhood_setter = LocalNeighbourhoodDAOFactory.create_setter(local_neighbourhood)

            # Configure inout datastore)
            inout_datastore = config["inout-datastore"]

            user = output_datastore["Users"]
            friend = inout_datastore["Friends"]

            user_setter = UserDAOFactory.create_setter(user)
            user_getter = UserDAOFactory.create_getter(user)

            user_friend_setter = UserFriendDAOFactory.create_setter(friend)
            user_friend_getter = UserFriendDAOFactory.create_getter(friend)

            user_downloader = TwitterUserDownloader(twitter_getter,
                user_setter)
            user_friends_downloader = FriendDownloader(twitter_getter,
                user_friend_setter, user_setter)

            local_neighbourhood_downloader = LocalNeighbourhoodDownloader(
                user_downloader, user_friends_downloader, user_getter,
                user_friend_getter, local_neighbourhood_setter)

            self.local_neighbourhood_downloader = local_neighbourhood_downloader

    def download_local_neighbourhood_by_screen_name(self, screen_name: str, params=None):
        self.local_neighbourhood_downloader.download_local_neighbourhood_by_screen_name(screen_name, params)
