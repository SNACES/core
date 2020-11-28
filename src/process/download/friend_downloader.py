from src.dao.twitter.tweepy_twitter_dao import TweepyTwitterGetter
from src.dao.user_friend.setter.friend_setter import FriendSetter

# TODO clean up all comments (change follower to friend etc.)

class FriendDownloader():
    """
    Download Twitter Followers for use in future algorithms.
    """
    def __init__(self, twitter_getter, user_friend_setter, user_setter):
        self.twitter_getter = twitter_getter
        self.user_friend_setter = user_friend_setter
        self.user_setter = user_setter

    def download_friends_ids_by_id(self, user_id: str, num_friends=0) -> None:
        """
        Gets a list of followers ids of a user by id
        """
        id, followers_user_ids = self.twitter_getter.get_friends_ids_by_user_id(user_id, num_friends=num_friends)
        self.user_friend_setter.store_friends(id, followers_user_ids)

    def download_friends_ids_by_screen_name(self, screen_name: str, num_friends=0) -> None:
        """
        """
        id, followers_user_ids = self.twitter_getter.get_friends_ids_by_screen_name(screen_name, num_friends=num_friends)
        self.user_friend_setter.store_friends(id, followers_user_ids)

    def download_friends_users_by_id(self, user_id: str, num_friends=0) -> None:
        """
        Gets a list of followers of a user by id

        @param user_id the id of the user to query on
        @param num_followers the maximum number of followers to retrieve

        @return a list of users who are friends of the given user
        """
        id, friends_users = self.twitter_getter.get_friends_users_by_user_id(user_id, num_friends=num_friends)

        self.user_setter.store_users(friends_users)

        friend_user_ids = [user.id for user in friends_users]
        self.user_friend_setter.store_friends(id, friend_user_ids)

    def download_friends_users_by_screen_name(self, screen_name: str, num_friends=0) -> None:
        """
        Gets a list of followers of a user by id

        @param user_id the id of the user to query on
        @param num_followers the maximum number of followers to retrieve

        @return a list of ids of followers for the given user
        """
        id, friends_users = self.twitter_getter.get_friends_users_by_screen_name(screen_name, num_friends=num_friends)

        self.user_setter.store_users(friends_users)

        friend_user_ids = [user.id for user in friends_users]
        self.user_friend_setter.store_friends(id, friend_user_ids)
