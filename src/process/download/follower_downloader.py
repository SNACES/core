from src.dao.twitter.tweepy_twitter_dao import TweepyTwitterGetter
from src.dao.user_follower.setter.follower_setter import FollowerSetter

class TwitterFollowerDownloader():
    """
    Download Twitter Followers for use in future algorithms.
    """
    def __init__(self, tweepy_getter, user_follower_setter, user_setter):
        self.tweepy_getter = tweepy_getter
        self.user_follower_setter = user_follower_setter
        self.user_setter = user_setter

    def download_followers_ids_by_id(self, user_id: str, num_followers=None) -> None:
        """
        """
        id, followers_user_ids = self.tweepy_getter.get_followers_ids_by_id(user_id)
        self.user_follower_setter.store_followers(id, followers_user_ids)

    def download_followers_ids_by_screen_name(self, screen_name: str, num_followers=None) -> None:
        """
        """
        id, followers_user_ids = self.tweepy_getter.get_followers_ids_by_screen_name(screen_name)
        self.user_follower_setter.store_followers(id, followers_user_ids)

    def download_followers_users_by_id(self, user_id: str, num_followers=None) -> None:
        """
        Gets a list of followers of a user by id

        @param user_id the id of the user to query on
        @param num_followers the maximum number of followers to retrieve

        @return a list of ids of followers for the given user
        """
        id, followers_users = self.tweepy_getter.get_followers_users_by_id(id, num_followers)

        self.user_setter.store_users(followers_users)

        follower_user_ids = [user.id for user in followers_users]
        self.user_follower_setter.store_followers(id, follower_user_ids)

    def download_followers_users_by_screen_name(self, screen_name: str, num_followers=None) -> None:
        """
        Gets a list of followers of a user by id

        @param user_id the id of the user to query on
        @param num_followers the maximum number of followers to retrieve

        @return a list of ids of followers for the given user
        """
        id, followers_users = self.tweepy_getter.get_followers_users_by_screen_name(screen_name, num_followers)

        self.user_setter.store_users(followers_users)

        follower_user_ids = [user.id for user in followers_users]
        self.user_follower_setter.store_followers(id, follower_user_ids)
