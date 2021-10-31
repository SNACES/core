from src.model.user import User
from src.shared.utils import cosine_sim
from typing import Dict, List


class DetectCommunityActivity():
    """
    Given a seed set of users, find a community expanded from the seed set
    """

    def __init__(self, user_getter, user_downloader, user_friends_downloader,
            user_tweets_downloader, user_friends_getter, community_ranker):
        self.user_getter = user_getter
        self.user_downloader = user_downloader
        self.user_friends_downloader = user_friends_downloader
        self.user_tweets_downloader = user_tweets_downloader
        self.user_friends_getter = user_friends_getter
        self.community_ranker = community_ranker

    def detect_community_by_screen_name(self, screen_names: List):
        user_ids = []
        for names in screen_names:
            user = self.user_getter.get_user_by_screen_name(names)
            user_ids.append(user.id)
        self.detect_community(user_ids)

    def detect_community(self, seed_set: List, iteration = 1):
        current_community = seed_set
        new_added_users = seed_set

        for _ in iteration:
            current_community, new_added_users = self.loop(current_community, new_added_users)
        return current_community

    def loop(self, current_community: List, new_added_users: List):
        for user_id in new_added_users:
            self.user_downloader.download_user_by_id(user_id)
            self.user_friends_downloader.download_friends_users_by_id(user_id)
        self.user_tweets_downloader.download_user_tweets_by_user_list(new_added_users)

        local_expansion = []
        for user_id in new_added_users:
            local_expansion.extend(self.user_friends_getter.get_user_friends_ids(user_id))

        ranked_ids = self.community_ranker.rank(local_expansion)
        added_users = []

        i = 0
        while (len(added_users) <= 10) and (ranked_ids[i] not in current_community):
            added_users.append(ranked_ids[i])
            i += 1
        
        current_community.extend(added_users)

        print(current_community)

        return current_community, added_users
