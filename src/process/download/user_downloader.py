from src.dao.twitter.twitter_dao import TwitterGetter
from src.dao.user.setter.user_setter import UserSetter


class TwitterUserDownloader():
    """
    Downloads a twitter User
    """

    def __init__(self, twitter_getter: TwitterGetter, user_setter: UserSetter):
        self.twitter_getter = twitter_getter
        self.user_setter = user_setter

    def download_user_by_screen_name(self, screen_name: str):
        user = self.twitter_getter.get_user_by_screen_name(screen_name)
        self.user_setter.store_user(user)

    def download_user_by_id(self, user_id: int):
        user = self.twitter_getter.get_user_by_id(user_id)
        self.user_setter.store_user(user)
