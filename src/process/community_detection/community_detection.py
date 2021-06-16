from src.model.user import User
from src.shared.utils import cosine_sim
from typing import Dict, List
from src.shared.logger_factory import LoggerFactory

log = LoggerFactory.logger(__name__)


class CommunityDetector():
    """
    Given a seed set of users, find a community expanded from the seed set
    fields:
    user_getter: see src/dao/user/getter/mongo_user_getter.py
                API: get_user_by_id(id), get_user_by_screen_name(screen_name)
    """

    def __init__(self, user_getter, user_downloader, user_friends_downloader,
            user_tweets_downloader, user_friends_getter, community_retweet_ranker, 
            community_tweet_ranker, community_setter, community_ranker):
        self.user_getter = user_getter
        self.user_downloader = user_downloader
        self.user_friends_downloader = user_friends_downloader
        self.user_tweets_downloader = user_tweets_downloader
        self.user_friends_getter = user_friends_getter
        self.community_retweet_ranker = community_retweet_ranker
        self.community_tweet_ranker = community_tweet_ranker
        self.community_setter = community_setter
        self.community_ranker = community_ranker

    def detect_community_by_screen_name(self, screen_names: List):
        """ detect community entrance method
        @param screen_names: a list of strings, being the seed users set of the community detection algorithm.
        """
        users = []
        for names in screen_names:
            user = self.user_getter.get_user_by_screen_name(names)
            users.append(user)
        self.detect_community(users)

    def detect_community(self, seed_set: List, iteration = 10):
        """
        @param seed_set: a list of users (i.e. type: src.model.user.User)
        @param iteration: the number of iterations we will perform
        """
        current_community = seed_set
        new_added_users = seed_set
        expansion = []

        for index in range(iteration):
            log.info(f"iteration index: {index + 1} / {iteration}")
            current_community, new_added_users, expansion = self.loop(current_community,
                                                                      new_added_users, expansion, index + 1)
        return current_community

    def loop(self, current_community: List, new_added_users: List, expansion: List, iteration):
        """
        @param current_community: list of users, the detected community
        @param new_added_users: list of users, the new users to expand
        @param expansion: list of users,
        """
        log.info(f"Start Downloading information for new added users")
        for user in new_added_users:
            log.info(f"Downloading New Added User: {user.screen_name}")
            self.user_downloader.download_user_by_id(user.id)
            log.info(f"Downloading User Friends of {user.screen_name}")
            self.user_friends_downloader.download_friends_users_by_id(user.id)
            log.info(f"Finished downloading friends of {user.screen_name}")

        log.info(f'Finish downloading all user friends')

        # Download tweets for users, no need now
        # self.user_tweets_downloader.download_user_tweets_by_user_list(new_added_users)
        # log.info("Downloading User Tweets for new added users")
        # for user in new_added_users:
        #     log.info(f'Start to download tweets of user {user.screen_name}')
        #     self.user_tweets_downloader.download_user_tweets_by_user(user)
        #     log.info(f'Finish downloading tweets of user {user.screen_name}')
        #
        # log.info('DONE!!!!!!!')

        # Do some data cleaning, eliminate users
        # Use Data.Friends, only keep those users appear most frequently in the friend_lists
        # We stop adding more users as long as we have got 500 users already
        friend_id_to_occurrence = dict()
        for user in new_added_users:
            friend_list = self.user_friends_getter.get_user_friends_ids(user.id)
            for friend_id in friend_list:
                if friend_id in friend_id_to_occurrence:
                    friend_id_to_occurrence[friend_id] += 1
                else:
                    friend_id_to_occurrence[friend_id] = 1

        occurrence_to_friend_id = dict()
        for value in range(1, len(new_added_users) + 1):
            occurrence_to_friend_id[value] = []
        for key, value in friend_id_to_occurrence.items():
            occurrence_to_friend_id[value].append(key)
        count = 0
        local_expansion = expansion
        for i in range(len(new_added_users), 0, -1):
            count += len(occurrence_to_friend_id[i])
            local_expansion.extend(occurrence_to_friend_id[i])
            if count >= 500:
                break
        log.info(f'Finish expanding the community, {count} users are added to the candidate pool')

        # Rank candidates
        log.info("Start ranking users")
        ranked_ids = self.community_ranker.rank(local_expansion, current_community)

        # pick top candidates
        added_users = []
        for id in ranked_ids:
            new_user_flag = True
            for user in current_community:
                if id == user.id:
                    new_user_flag = False
                    break
            if new_user_flag:
                added_users.append(self.user_getter.get_user_by_id(id))
            if len(added_users) == 10:
                break
        current_community.extend(added_users)

        log.info("Store information for community detection")
        self.community_setter.store_community(iteration,
                                              [user.id for user in added_users],
                                              [user.id for user in current_community])

        log.info('New Added Users:')
        for user in added_users:
            print(f'{user.screen_name}', end=' ')
        print()
        return current_community, new_added_users, local_expansion

        # log.info("Rank Users by tweet")
        # ranked_ids = self.community_tweet_ranker.rank(local_expansion, current_community)
        #
        # ranked_ids_by_retweet = self.community_retweet_ranker.rank(local_expansion, current_community)
        #
        # added_users = []
        #
        # cleaned_added_users = []
        # for uu in ranked_ids:
        #     if uu in ranked_ids_by_retweet[:int(len(ranked_ids_by_retweet)/3)]:
        #         cleaned_added_users.append(uu)
        #
        # i = 0
        # while len(added_users) < 10 and i < len(cleaned_added_users):
        #     if cleaned_added_users[i] not in current_community:
        #         added_users.append(cleaned_added_users[i])
        #     i += 1
        #
        # log.info("Store information for community detection")
        # self.community_setter.store_community(iteration, added_users, current_community)
        #
        # current_community.extend(added_users)
        #
        # print(current_community)
        #
        # return current_community, added_users, local_expansion