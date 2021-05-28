from src.model.user import User
from src.shared.utils import cosine_sim
from typing import Dict, List
from src.shared.logger_factory import LoggerFactory

log = LoggerFactory.logger(__name__)


class CommunityDetector():
    """
    Given a seed set of users, find a community expanded from the seed set
    """

    def __init__(self, user_getter, user_downloader, user_friends_downloader,
            user_tweets_downloader, user_friends_getter, community_retweet_ranker, 
            community_tweet_ranker, community_setter):
        self.user_getter = user_getter
        self.user_downloader = user_downloader
        self.user_friends_downloader = user_friends_downloader
        self.user_tweets_downloader = user_tweets_downloader
        self.user_friends_getter = user_friends_getter
        self.community_retweet_ranker = community_retweet_ranker
        self.community_tweet_ranker = community_tweet_ranker
        self.community_setter = community_setter

    def detect_community_by_screen_name(self, screen_names: List):
        user_ids = []
        for names in screen_names:
            user = self.user_getter.get_user_by_screen_name(names)
            user_ids.append(user.id)
        self.detect_community(user_ids)

    def detect_community(self, seed_set: List, iteration = 10):
        current_community = seed_set
        new_added_users = seed_set
        expansion = []

        for index in range(iteration):
            log.info("iteration index")
            current_community, new_added_users, expansion = self.loop(current_community, new_added_users, expansion, index+1)
        return current_community

    def loop(self, current_community: List, new_added_users: List, expansion: List, iteration: int):
        log.info("Downloading information for new added users")
        for user_id in new_added_users:
            log.info("Downloading New Added User" + str(user_id))
            self.user_downloader.download_user_by_id(user_id)
            log.info("Downloading User Friends")
            self.user_friends_downloader.download_friends_users_by_id(user_id)
        log.info("Downloading User Tweets for new added users")
        self.user_tweets_downloader.download_user_tweets_by_user_list(new_added_users)

        local_expansion = expansion
        for user_id in new_added_users:
            log.info("Expand the community to get candidate users for user" + str(user_id))
            candidate_friends = self.user_friends_getter.get_user_friends_ids(user_id)
            local_expansion.extend(candidate_friends)

        log.info("Rank Users by tweet")
        ranked_ids = self.community_tweet_ranker.rank(local_expansion, current_community)

        ranked_ids_by_retweet = self.community_retweet_ranker.rank(local_expansion, current_community)

        added_users = []

        cleaned_added_users = []
        for uu in ranked_ids:
            if uu in ranked_ids_by_retweet[:int(len(ranked_ids_by_retweet)/3)]:
                cleaned_added_users.append(uu)

        i = 0
        while len(added_users) < 10 and i < len(cleaned_added_users):
            if cleaned_added_users[i] not in current_community:
                added_users.append(cleaned_added_users[i])
            i += 1

        log.info("Store information for community detection")
        self.community_setter.store_community(iteration, added_users, current_community)

        current_community.extend(added_users)

        print(current_community)

        return current_community, added_users, local_expansion