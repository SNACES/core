from typing import List

from src.shared.logger_factory import LoggerFactory

log = LoggerFactory.logger(__name__)
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
        id, followers_user_ids = self.tweepy_getter.get_followers_ids_by_user_id(user_id)
        log.info(f"Downloaded {len(followers_user_ids)} Followers for user {user_id}")
        self.user_follower_setter.store_followers(id, followers_user_ids)

    def download_followers_ids_by_id_list(self, ids: List[str]) -> None:
        """
        """
        num_ids = len(ids)
        count = 0

        # for user_id in ids:
        #     if not self.user_follower_setter._contains_user(user_id):
        #         log.info(f"Downloading followers for {user_id}...")
        #         self.download_followers_ids_by_id(user_id)
        #     else:
        #         log.info(f"Skipped user {user_id} because followers are already downloaded")
        #     count += 1
        #     log.log_progress(log, count, num_ids)

        for a in range(len(ids)):
            for b in range(a+1, len(ids)):
                a_follow_b, b_follow_a = self.tweepy_getter.check_friendship(ids[a], ids[b])
                self.user_follower_setter.store_followers(ids[a], ids[b], a_follow_b, b_follow_a)
            count += 1
            log.info(f"Downloaded Friendships for user {a}")
            log.log_progress(log, count, num_ids)


    def download_followers_ids_by_screen_name(self, screen_name: str, num_followers=None) -> None:
        """
        """
        id, followers_user_ids = self.tweepy_getter.get_followers_ids_by_screen_name(screen_name)
        self.user_follower_setter.store_followers(id, followers_user_ids)

    def download_followers_users_by_id(self, user_id: str) -> None:
        """
        Gets a list of followers of a user by id

        @param user_id the id of the user to query on
        @param num_followers the maximum number of followers to retrieve

        @return a list of ids of followers for the given user
        """
        followers_users = self.tweepy_getter.get_followers_users_by_id(user_id)
        self.user_follower_setter.store_followers(user_id, followers_users)

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
