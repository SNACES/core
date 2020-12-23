from typing import Dict
from src.shared.mongo import get_collection_from_config
from src.dao.twitter.tweepy_twitter_dao import TweepyTwitterGetter
from src.dao.user_follower.setter.mongo_follower_setter import MongoFollowerSetter


class DownloadUserFollowersActivity():
    def __init__(self, config: Dict):
        self.follower_downloader = None
        self.configure(config)

    def configure(self, config: Dict):
        if config is not None:
            tweepy_getter = TweepyTwitterGetter()
            user_follower_setter = MongoFollowerSetter()

            collection = get_collection_from_config(config)

            user_follower_setter.set_follower_collection(collection)

            self.follower_downloader = MongoFollowerSetter(tweepy_getter, user_follower_setter)

    def download_followers_by_id(self, user_id: str) -> None:
        self.follower_downloader.download_followers_by_id(user_id)

    def download_followers_by_screen_name(self, user_id: str) -> None:
        self.follower_downloader.download_followers_by_id(user_id)
