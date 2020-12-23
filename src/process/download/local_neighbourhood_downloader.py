from src.process.download.user_downloader import TwitterUserDownloader
from src.process.download.friend_downloader import FriendDownloader
from src.dao.user.getter.user_getter import UserGetter
from src.dao.user_friend.getter.friend_getter import FriendGetter
from src.dao.local_neighbourhood.setter.local_neighbourhood_setter import LocalNeighbourhoodSetter
from src.model.local_neighbourhood import LocalNeighbourhood
from typing import Dict

class LocalNeighbourhoodDownloader():
    def __init__(self, user_downloader: TwitterUserDownloader,
            user_friends_downloader: FriendDownloader,
            user_getter: UserGetter,
            user_friend_getter: FriendGetter,
            local_neighbourhood_setter: LocalNeighbourhoodSetter):
        self.user_downloader = user_downloader
        self.user_friends_downloader = user_friends_downloader

        self.user_getter = user_getter
        self.user_friend_getter = user_friend_getter
        self.local_neighbourhood_setter = local_neighbourhood_setter

    def download_local_neighbourhood_by_screen_name(self, screen_name: str, params=None):
        self.user_downloader.download_user_by_screen_name(screen_name)
        user = self.user_getter.get_user_by_screen_name(screen_name)

        user_friends_ids = self.user_friend_getter.get_user_friends_ids(user.id)
        if user_friends_ids is None:
            self.user_friends_downloader.download_friends_ids_by_id(user.id)
            user_friends_ids = self.user_friend_getter.get_user_friends_ids(user.id)

        user_dict = {}
        user_dict[str(user.id)] = user_friends_ids

        for id in user_friends_ids:
            user_friends = self.user_friend_getter.get_user_friends_ids(id)
            if user_friends is None:
                self.user_friends_downloader.download_friends_ids_by_id(id)
                user_friends = self.user_friend_getter.get_user_friends_ids(id)

            user_dict[str(id)] = [id for id in user_friends if (id in user_friends_ids)]

        local_neighbourhood = LocalNeighbourhood(seed_id=user.id, params=params, users=user_dict)
        self.local_neighbourhood_setter.store_local_neighbourhood(local_neighbourhood)
