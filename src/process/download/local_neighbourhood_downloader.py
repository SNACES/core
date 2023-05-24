from src.process.download.user_downloader import TwitterUserDownloader
from src.process.download.friend_downloader import FriendDownloader
from src.dao.user.getter.user_getter import UserGetter
from src.dao.user_activity.getter.user_activity_getter import ActivityGetter
from src.dao.user_friend.getter.friend_getter import FriendGetter
from src.dao.local_neighbourhood.setter.local_neighbourhood_setter import LocalNeighbourhoodSetter
from src.model.local_neighbourhood import LocalNeighbourhood
from src.shared.utils import print_progress
from typing import Dict
import math
from src.process.data_cleaning import extended_friends_cleaner

from src.shared.logger_factory import LoggerFactory

log = LoggerFactory.logger(__name__)


class LocalNeighbourhoodDownloader():
    def __init__(self, user_downloader: TwitterUserDownloader,
                 user_friends_downloader: FriendDownloader,
                 user_getter: UserGetter,
                 user_friend_getter: FriendGetter,
                 user_activity_getter: ActivityGetter,
                 cleaned_user_friend_getter: FriendGetter,
                 local_neighbourhood_setter: LocalNeighbourhoodSetter,
                 user_activity: str):
        self.user_downloader = user_downloader
        self.user_friends_downloader = user_friends_downloader
        self.user_friend_getter = user_friend_getter
        self.user_getter = user_getter
        self.user_activity_getter = user_activity_getter
        self.cleaned_user_friend_getter = cleaned_user_friend_getter
        self.local_neighbourhood_setter = local_neighbourhood_setter
        self.user_activity = user_activity

    def download_local_neighbourhood_by_id(self, user_id: str, params=None, clean=True):
        # user_friends_ids = self.cleaned_user_friend_getter.get_user_friends_ids(user_id)
        # if user_friends_ids is None:
        #     log.info("Could not find user_friend list")
        #     self.user_friends_downloader.download_friends_ids_by_id(user_id)
        user_friends_ids = self.user_friend_getter.get_user_friends_ids(
            user_id)

        log.info(f"{ user_id} has {len(user_friends_ids)} friends")
        if clean:
            user_friends_ids, t = self.clean_user_friends_global(
                user_id, user_friends_ids)

        user_dict = {}
        user_dict[str(user_id)] = user_friends_ids

        num_ids = len(user_friends_ids)
        log.info(f"Cleaning Threshold: {t}")
        log.info("Starting Downloading Friend List for " +
                 str(len(user_friends_ids)) + " users")
        for i in range(num_ids):
            id = user_friends_ids[i]

            user_activities = self.user_activity_getter.get_user_activities(id)
            if user_activities is None:
                # self.user_friends_downloader.download_friends_ids_by_id(id)
                # user_friends = self.user_friend_getter.get_user_friends_ids(id)
                # log.info("Downloaded " + str(len(user_friends)) + " user friends for " + str(id))
                user_activities = []
                log.info("Could not get user activities for " + str(id))
            else:
                log.info("Already stored " + str(len(user_activities)) +
                         " user friends for " + str(id))

            assert user_activities is not None

            user_dict[str(id)] = [str(id)
                                  for id in user_activities if (id in user_friends_ids)]

            log.log_progress(log, i, num_ids)

        local_neighbourhood = LocalNeighbourhood(
            seed_id=user_id, params=params, users=user_dict, user_activity=self.user_activity)
        self.local_neighbourhood_setter.store_local_neighbourhood(
            local_neighbourhood)

        log.info("Done downloading local neighbourhood")

    def download_local_neighbourhood_by_screen_name(self, screen_name: str, params=None):
        log.info("Downloading local neighbourhood of " + str(screen_name))

        self.user_downloader.download_user_by_screen_name(screen_name)
        id = self.user_getter.get_user_by_screen_name(screen_name).get_id()

        self.download_local_neighbourhood_by_id(id, params)

    def clean_user_friends_global(self, user_id, friends_list):
        user = self.user_getter.get_user_by_id(str(user_id))
        log.info("Cleaning Friends List by Follower and Friend")
        t = 0.1

        num_users = len(friends_list)
        clean_friends_list = friends_list
        while (num_users > 1000):
            num_users = len(friends_list)
            clean_friends_list = []
            follower_thresh = t * user.followers_count
            friend_thresh = t * user.friends_count
            print(
                f"Data cleaning with thresholds {follower_thresh, friend_thresh}")
            for id in friends_list:
                num_users -= 1
                curr_user = self.user_getter.get_user_by_id(id)
                if user is not None and curr_user is not None and curr_user.followers_count > follower_thresh and curr_user.friends_count > friend_thresh:
                    clean_friends_list.append(id)
                    num_users += 1
            log.info(
                f"Increasing Data Cleaning Strength {t}, {num_users} remaining users")
            t += 0.05
        return clean_friends_list, t
