from src.model.user import User
from src.shared.utils import cosine_sim
from typing import Dict, List
from src.shared.logger_factory import LoggerFactory
from tqdm import tqdm

log = LoggerFactory.logger(__name__)


class CommunityDetector():
    """
    Given a seed set of users, find a community expanded from the seed set
    fields:
    user_getter: see src/dao/user/getter/mongo_user_getter.py
                API: get_user_by_id(id), get_user_by_screen_name(screen_name)
    """

    def __init__(self, user_getter, user_downloader, user_friends_downloader,
            user_tweets_downloader, user_friends_getter, community_production_ranker,
            community_consumption_ranker, community_setter, friends_cleaner, cleaned_friends_getter, user_tweets_getter):
        self.user_getter = user_getter
        self.user_downloader = user_downloader
        self.user_friends_downloader = user_friends_downloader
        self.user_tweets_downloader = user_tweets_downloader
        self.user_friends_getter = user_friends_getter
        self.community_production_ranker = community_production_ranker
        self.community_consumption_ranker = community_consumption_ranker
        self.community_setter = community_setter
        self.friends_cleaner = friends_cleaner
        self.cleaned_friends_getter = cleaned_friends_getter
        self.user_tweets_getter = user_tweets_getter

    def detect_community_by_screen_name(self, screen_names: List):
        """ detect community entrance method
        @param screen_names: a list of strings, being the seed users set of the community detection algorithm.
        """
        users = []
        print(screen_names)
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
            return
        return current_community

    def loop(self, current_community: List, new_added_users: List, expansion: List, iteration):
        """
        @param current_community: list of users, the detected community
        @param new_added_users: list of users, the new users to expand
        @param expansion: list of users,
        """
        log.info(f"Start Downloading information for new added users")
        for user in new_added_users:
            if self.cleaned_friends_getter.contains_user(user.id):
                log.info(f"Friends of User {user.screen_name} have been cleaned, skip to the next")
                continue
            log.info(f"Downloading New Added User: {user.screen_name}")
            self.user_downloader.download_user_by_id(user.id)
            log.info(f"Downloading User Friends of {user.screen_name}")
            self.user_friends_downloader.download_friends_users_by_id(user.id)
            log.info(f"Finished downloading friends of {user.screen_name}")

            init_friend_list = self.user_friends_getter.get_user_friends_ids(user.id)
            self.friends_cleaner.clean_friends_global(user.id, init_friend_list, tweet_threshold=100,
                                                      follower_threshold=1000, friend_threshold=50, bot_threshold=0)
            log.info(f"Finished cleaning friends of {user.screen_name}")

        log.info(f'Finish downloading and cleaning all user friends')

        # Do more data cleaning, eliminate users
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
        # local_expansion = expansion
        local_expansion = []
        for i in range(len(new_added_users), 0, -1):
            count += len(occurrence_to_friend_id[i])
            local_expansion.extend(occurrence_to_friend_id[i])
            if count >= 500:
                break
        log.info(f'Finish expanding the community, {count} users are added to the candidate pool')

        # # plot
        # import seaborn as sns
        # from scipy.stats import norm
        # norm.rvs()
        # num_follower_list = []
        # for key, value in occurrence_to_friend_id.items():
        #     print(f'{len(value)} users are followed by {key} users in the initial set')

        # Download tweets for users
        from datetime import datetime
        cnt = 0
        dic = {}
        log.info("Downloading User Tweets for new added users")
        for userid in tqdm(local_expansion):
            # tweets = self.user_tweets_getter.get_tweets_by_user_id(userid)
            # if len(tweets) >= 3200:
            #     cnt += 1
            #     try:
            #         created_str = tweets[-1].created_at
            #         mon = created_str[4:7]
            #         if mon in dic:
            #             dic[mon] += 1
            #         else:
            #             dic[mon] = 1
            #
            #         print(f'Mon = {mon}, User = {userid}')
            #     except:
            #         pass
            #     continue

            if self.user_tweets_getter.get_tweets_by_user_id(userid):
                print(f'Tweets of user {userid} has been downloaded, skip to next')
                continue
            log.info(f'Start to download tweets of user {userid}')
            self.user_tweets_downloader.download_user_tweets_by_user_id(userid)
            log.info(f'Finish downloading tweets of user {userid}')

        log.info('Finish downloading all tweets')
        return
        # print(f'{cnt} users out of {len(local_expansion)} has 3200 tweets')
        # print(dic)
        # Rank candidates
        log.info("Start ranking users")


        current_community_id_list = [user.id for user in current_community]
        score = self.community_retweet_ranker.score_users(local_expansion, current_community_id_list)
        print(f'score = {score}')

        ranked_ids = self.community_retweet_ranker.rank(local_expansion, current_community_id_list)
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