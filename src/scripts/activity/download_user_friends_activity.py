from typing import Dict
from src.shared.mongo import get_collection_from_config
from src.dao.twitter.twitter_dao_factory import TwitterDAOFactory
from src.dao.user.user_dao_factory import UserDAOFactory
from src.dao.user_friend.user_friend_dao_factory import UserFriendDAOFactory
from src.process.download.friend_downloader import FriendDownloader

class DownloadUserFriendsActivity():
    def __init__(self, config: Dict):
        self.friend_downloader = None
        self.configure(config)

    def configure(self, config: Dict):
        if config is not None:
            # Configure input datastore
            input_datastore = config["input-datastore"]
            download_source = input_datastore["Download-Source"]

            twitter_getter = TwitterDAOFactory.create_getter(download_source)

            # Configure output datastore
            output_datastore = config["output-datastore"]
            users = output_datastore["Users"]

            user_setter = UserDAOFactory.create_setter(users)

            friends = output_datastore["Friends"]

            user_friend_setter = UserFriendDAOFactory.create_setter(friends)

            self.friend_downloader = FriendDownloader(twitter_getter, user_friend_setter, user_setter)

    def download_friends_by_id(self, user_id: str, saturated=False) -> None:
        if saturated:
            self.friend_downloader.download_friends_users_by_id(user_id)
        else:
            self.friend_downloader.download_friends_ids_by_id(user_id)

    def download_friends_by_screen_name(self, screen_name: str, saturated=False) -> None:
        if saturated:
            self.friend_downloader.download_friends_users_by_screen_name(screen_name)
        else:
            self.friend_downloader.download_friends_ids_by_screen_name(screen_name)
