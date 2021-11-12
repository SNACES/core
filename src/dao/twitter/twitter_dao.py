from src.model.user import User
from typing import Dict, List


class TwitterGetter():
    def stream_tweets(self, num_tweets, subscriber) -> None:
        raise NotImplementedError("Subclasses should implement this")

    def buffered_stream_tweets(self, num_tweets, subscriber) -> None:
        raise NotImplementedError("Subclasses should implement this")

    def get_tweets_by_user_id(self, user_id: str, num_tweets=0):
        raise NotImplementedError("Subclasses should implement this")

    def get_liked_tweets_by_user_id(self, user_id: str):
        raise NotImplementedError("Subclasses should implement this")

    def get_user_by_id(self, user_id: str) -> User:
        raise NotImplementedError("Subclasses should implement this")

    def get_user_by_screen_name(self, screen_name: str) -> User:
        raise NotImplementedError("Subclasses should implement this")

    def get_friends_ids_by_user_id(self, user_id: str, num_friends=0) -> List[str]:
        raise NotImplementedError("Subclasses should implement this")

    def get_friends_users_by_user_id(self, user_id: str, num_friends=0) -> List[str]:
        raise NotImplementedError("Subclasses should implement this")

    def get_followers_ids_by_user_id(self, user_id: str, num_followers=0) -> List[User]:
        raise NotImplementedError("Subclasses should implement this")

    def get_users_by_user_id_list(self, user_id_list: List[str]) -> List[User]:
        return [self.get_users_by_id(user_id) for user_id in user_id_list]

    def get_tweets_by_screen_name(self, screen_name: str, num_tweets=0):
        user = self.get_user_by_screen_name(screen_name)
        return self.get_tweets_by_user_id(user.id)

    def get_friends_ids_by_screen_name(self, screen_name: str, num_friends=0) -> List[User]:
        user = self.get_user_by_screen_name(screen_name)
        return self.get_friends_ids_by_user_id(user.id, num_friends=num_friends)

    def get_followers_ids_by_screen_name(self, screen_name: str, num_followers=0) -> List[User]:
        user = self.get_user_by_screen_name(screen_name)
        return self.get_followers_by_id(user.id, num_followers=num_followers)

    def get_friends_users_by_screen_name(self, screen_name: str, num_friends=0) -> List[User]:
        user = self.get_user_by_screen_name(screen_name)
        return self.get_friends_users_by_user_id(user.id, num_friends=num_friends)

    def get_followers_users_by_screen_name(self, screen_name: str, num_followers=0) -> List[User]:
        user = self.get_user_by_screen_name(screen_name)
        return self.get_followers_users_by_id(user.id, num_followers=num_followers)
