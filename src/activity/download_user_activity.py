from typing import Dict
from src.shared.mongo import get_collection_from_config
from src.dao.twitter.twitter_dao_factory import TwitterDAOFactory
from src.dao.user.user_dao_factory import UserDAOFactory
from src.process.download.user_downloader import TwitterUserDownloader

class DownloadUserActivity():
    def __init__(self, config: Dict):
        self.user_downloader = None
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

            self.user_downloader = TwitterUserDownloader(twitter_getter,
                user_setter)

    def download_user_by_id(self, user_id:str):
        self.user_downloader.download_user_by_id(user_id)

    def download_user_by_screen_name(self, screen_name: str):
        self.user_downloader.download_user_by_screen_name(screen_name)
