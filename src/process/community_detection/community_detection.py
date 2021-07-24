from src.model.user import User
from src.shared.utils import cosine_sim
from typing import Dict, List
from src.shared.logger_factory import LoggerFactory
from tqdm import tqdm
import json
import seaborn as sns
from matplotlib import pyplot as plt
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
            init_friend_list = self.friends_cleaner.clean_friends_global(user.id, init_friend_list, tweet_threshold=100,
                                                      follower_threshold=1000, friend_threshold=200, bot_threshold=0)
            log.info(f"Finished cleaning friends of {user.screen_name}")
        log.info(f'Finish downloading and cleaning all user friends')

        # Do more data cleaning, eliminate users
        # Use Data.Friends, only keep those users appear most frequently in the friend_lists
        # We stop adding more users as long as we have got 500 users already
        friend_id_to_occurrence = dict()
        for user in new_added_users:
            # friend_list = self.user_friends_getter.get_user_friends_ids(user.id)
            friend_list = self.cleaned_friends_getter.get_user_friends_ids(user.id)

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

        local_expansion_candidate = []
        for i in range(len(new_added_users), 0, -1):
            count += len(occurrence_to_friend_id[i])
            local_expansion_candidate.extend(occurrence_to_friend_id[i])
            print(f'Add {len(occurrence_to_friend_id[i])} users of followers overlap = {i}')

            # if i == 3 or count >= 500:
            #     break
        # # following back
        # follow_back_dict = {}
        # for userid in local_expansion_candidate:
        #     self.user_friends_downloader.download_friends_users_by_id(userid)
        #     friends = self.user_friends_getter.get_user_friends_ids(userid)
        #     if friends is not None:
        #         num_follow_back = 0
        #         for community_member in current_community:
        #             if int(community_member.id) or str(community_member.id) in friends:
        #                 num_follow_back += 1
        #         if num_follow_back in follow_back_dict:
        #             follow_back_dict[num_follow_back] += 1
        #         else:
        #             follow_back_dict[num_follow_back] = 1
        # print(f'follow back = {follow_back_dict}')

        # Local Cleaning
        # for userid in tqdm(local_expansion_candidate):
        #     self.user_friends_downloader.download_friends_users_by_id(userid)
        #     friend_list = self.user_friends_getter.get_user_friends_ids(userid)
        #     print(len(friend_list))
        #     clean_friends_list, deleted_friends = self.friends_cleaner.clean_friends_local(userid, friend_list)
        #     print(f'{len(deleted_friends)} are eliminated in local cleaning for {userid}')

        log.info(f'Finish expanding the community, {count} users are added to the candidate pool')

        # Download tweets for users
        # log.info("Downloading User Tweets for new added users")
        # for userid in tqdm(local_expansion_candidate):      # CHANGE BACK TO local_expansion later
        #     if self.user_tweets_getter.get_tweets_by_user_id(userid):
        #         print(f'Tweets of user {userid} has been downloaded, skip to next')
        #         self.user_tweets_getter.convert_dates_for_user_id(userid)
        #         continue
        #     log.info(f'Start to download tweets of user {userid}')
        #     self.user_tweets_downloader.download_user_tweets_by_user_id(userid)
        #     self.user_tweets_getter.convert_dates_for_user_id(userid)
        #     log.info(f'Finish downloading tweets of user {userid}')
        # log.info('Finish downloading all tweets')

        # Get the reference set from file
        REF_SIZE = 100    # the size of the reference set
        file_name = f'./dc2_exp/production_rankings/local_5.0_global_50/hardmaru_all_cluster_1.json'
        file_name = f'./dc2_exp/production_no_scale_rankings/local_5.0_global_50/hardmaru_all_cluster_1.json'
        file_name = f'./dc2_exp/consumption_no_scale_rankings/local_5.0_global_50/hardmaru_all_cluster_1.json'

        with open(file_name) as f:
            raw_data = json.load(f)
            data = [int(userid) for userid in raw_data]
        reference_set = data[11: 11 + REF_SIZE]

        # Rank candidates
        log.info("Start ranking users")

        current_community_id_list = [user.id for user in current_community]

        # scores = self.community_production_ranker.score_users(
        #     local_expansion_candidate, UnionLists(current_community_id_list, reference_set))
        scores = self.community_consumption_ranker.score_users(
            local_expansion_candidate, UnionLists(current_community_id_list, reference_set))

        # scores = self.community_production_ranker.score_users(local_expansion, current_community_id_list)
        print(f'score = {scores}')
        ranked_ids = list(sorted(scores, key=scores.get, reverse=True))
        # ranked_ids = self.community_production_ranker.rank(local_expansion, current_community_id_list)

        # plot
        x_axis, y_axis = [], []
        for i, id in enumerate(ranked_ids):
            x_axis.append(i + 1)
            y_axis.append(scores[id])
        # plt.plot(x_axis, y_axis)
        # plt.xlabel('User Ranking')
        # plt.ylabel('Utility Value')
        # plt.title(f'Community Expansion Production Utility Value, Ref Size = {REF_SIZE}, Scale, Clean1')
        # plt.savefig(f'Production_{REF_SIZE}_scale_clean1.png')
        print(y_axis)

        # pick top candidates
        added_users = []
        for id in ranked_ids:
            new_user_flag = True
            for user in current_community:
                if str(id) == str(user.id):
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


def UnionLists(a: List, b: List):
    return list(set().union(a, b))