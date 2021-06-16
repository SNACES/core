import matplotlib.pyplot as plt
import numpy as np

from src.process.data_cleaning.extended_friends_cleaner import \
    ExtendedFriendsCleaner
from src.dao.user_friend.getter.friend_getter import FriendGetter
from src.dao.user.getter.user_getter import UserGetter
from src.shared.logger_factory import LoggerFactory

log = LoggerFactory.logger(__name__)

class DataCleaningDistributions():
    """
    Given a seed user, creates distributions of number of tweets, followers, etc
    of the users in the local neighborhood
    """
    def __init__(self, friends_getter: FriendGetter, user_getter: UserGetter,
                 friends_cleaner: ExtendedFriendsCleaner):
        self.friends_getter = friends_getter
        self.user_getter = user_getter
        self.friends_cleaner = friends_cleaner

    def tweet_plot(self, seed_id: str):
        friends = self.friends_getter.get_user_friends_ids(seed_id)

        log.info("Finished getting friend ids")
        friends.append(seed_id)
        num_tweets = []
        for friend in friends:
            user = self.user_getter.get_user_by_id(friend)
            num_tweets.append(user.statuses_count)
        log.info("Finished getting user counts")

        seed_user = self.user_getter.get_user_by_id(seed_id).screen_name

        plt.title('Tweet Distribution for ' + seed_user)
        plt.hist(num_tweets, cumulative=-1, density=True, bins=range(0, max(num_tweets) + 1, 1), histtype='stepfilled')
        log.info("Finished creating hist")
        plt.show()
        plt.savefig('tweet.png', dpi=300)

    def follower_plot(self, seed_id: str):
        friends = self.friends_getter.get_user_friends_ids(seed_id)
        friends.append(seed_id)
        num_followers = []
        for friend in friends:
            user = self.user_getter.get_user_by_id(friend)
            num_followers.append(user.followers_count)

        seed_user = self.user_getter.get_user_by_id(seed_id).screen_name

        plt.title('Followers Distribution for ' + seed_user)
        plt.hist(num_followers, cumulative=-1, density=True, bins=range(0, max(num_followers) + 1, 1), histtype='stepfilled')
        plt.show()
        plt.savefig('follower.png', dpi=300)
        plt.clf()

    def follower_ratio_plot(self, seed_id: str):
        friends = self.friends_getter.get_user_friends_ids(seed_id)
        friends.append(seed_id)
        ratios = []
        for friend in friends:
            user = self.user_getter.get_user_by_id(friend)
            if user.friends_count != 0:
                ratios.append(user.followers_count/user.friends_count)
            else:
                ratios.append(1000000)  # Just to indicate a high number

        seed_user = self.user_getter.get_user_by_id(seed_id).screen_name
        plt.title('Follower to Following Ratio Distribution for ' + seed_user)
        plt.hist(ratios, cumulative=-1, density=True, bins=np.arange(0, max(ratios) + 0.1, 0.1), histtype='stepfilled')
        plt.show()
        plt.savefig('ratio.png', dpi=300)
        plt.clf()

    def local_friends_plot(self, seed_id: str):
        friends = self.friends_getter.get_user_friends_ids(seed_id)

        local_count = []
        for friend in friends:
            count = 0
            user_friends = self.friends_getter.get_user_friends_ids(friend)
            for user in user_friends:
                if user in friends:
                    count += 1
            local_count.append(count)

        seed_user = self.user_getter.get_user_by_id(seed_id).screen_name

        plt.title('Local friends Distribution for ' + seed_user)
        plt.hist(local_count, cumulative=-1, density=True, bins=range(0, max(local_count) + 1, 1), histtype='stepfilled')
        plt.show()
        plt.savefig('local_friends.png', dpi=300)
        plt.clf()

    def local_friends_cutoff_plots(self, seed_id: str, global_thresh):
        init_friends = self.friends_getter.get_user_friends_ids(seed_id)
        counts = []
        thresholds = []
        friends = self.friends_cleaner.clean_friends_global(seed_id, init_friends, tweet_threshold=global_thresh,
                                                            follower_threshold=global_thresh, bot_threshold=0)
        for i in range(41):
            clean_friends, deleted_friends = self.friends_cleaner.clean_friends_local(seed_id, friends, local_follower=0, local_following=i)
            counts.append(len(clean_friends))
            thresholds.append(i)

        seed_user = self.user_getter.get_user_by_id(seed_id).screen_name

        plt.title('Remaining Friends after Locally Cleaning by Following for ' + seed_user + ' with Global Threshold Set to ' + str(global_thresh))
        plt.bar(thresholds, counts)
        plt.xlabel("Local Following Threshold")
        plt.ylabel("Number of Remaining Friends")
        plt.show()

    def local_friends_set_similarity(self, seed_id, local_thresh):
        init_friends = self.friends_getter.get_user_friends_ids(seed_id)
        counts = []
        thresholds = []
        prev_clean_friends, deleted_friends_initial = self.friends_cleaner.clean_friends_local(seed_id, init_friends,
                                                                           local_follower=0, local_following=local_thresh)
        for i in range(16):
            friends = self.friends_cleaner.clean_friends_global(seed_id, init_friends, tweet_threshold=10*i,
                                                            follower_threshold=10*i, bot_threshold=0)
            curr_clean_friends, deleted_friends = self.friends_cleaner.clean_friends_local(seed_id, friends, local_follower=0, local_following=local_thresh)
            counts.append(overlap(curr_clean_friends, prev_clean_friends))
            thresholds.append(i*10)
            prev_clean_friends = curr_clean_friends

        seed_user = self.user_getter.get_user_by_id(seed_id).screen_name
        log.info(counts)

        plt.title('Proportions of Remaining Friends from Previous Set for ' + seed_user + ' with Local Threshold Set to ' + str(local_thresh))
        plt.bar(thresholds, counts)
        plt.xlabel("Global Following Threshold")
        plt.ylabel("Proportion of Remaining Friends that are in Previous Set")
        plt.show()

    def local_friends_set_kept(self, seed_id, local_thresh):
        init_friends = self.friends_getter.get_user_friends_ids(seed_id)
        counts = []
        thresholds = []
        prev_clean_friends, deleted_friends_initial = self.friends_cleaner.clean_friends_local(seed_id, init_friends,
                                                                                               local_follower=0, local_following=local_thresh)
        for i in range(16):
            friends = self.friends_cleaner.clean_friends_global(seed_id, init_friends, tweet_threshold=10*i,
                                                                follower_threshold=10*i, bot_threshold=0)
            curr_clean_friends, deleted_friends = self.friends_cleaner.clean_friends_local(seed_id, friends, local_follower=0, local_following=local_thresh)
            counts.append(len(curr_clean_friends)/len(prev_clean_friends))
            thresholds.append(i*10)
            prev_clean_friends = curr_clean_friends

        seed_user = self.user_getter.get_user_by_id(seed_id).screen_name
        log.info(counts)

        plt.title('Proportion of Previous Set that is Kept ' + seed_user + ' with Local Threshold Set to ' + str(local_thresh))
        plt.bar(thresholds, counts)
        plt.xlabel("Global Following Threshold")
        plt.ylabel("Proportion of Previous Set that is Kept ")
        plt.show()

    def local_follower_distribution(self, seed_id, global_thresh, local_thresh):
        init_friends = self.friends_getter.get_user_friends_ids(seed_id)
        counts = []
        friends = self.friends_cleaner.clean_friends_global(seed_id, init_friends, tweet_threshold=global_thresh,
                                                            follower_threshold=global_thresh, bot_threshold=0)
        clean_friends, deleted_friends = self.friends_cleaner.clean_friends_local(seed_id, friends,
                                                                    local_follower=0, local_following=local_thresh)
        user_friends = {}
        for user in clean_friends:
            user_friends[user] = self.friends_getter.get_user_friends_ids(user)
        for user in clean_friends:
            local_followers = 0
            for friend in clean_friends:
                if user in user_friends[friend]:
                    local_followers += 1
            counts.append(local_followers)

        seed_user = self.user_getter.get_user_by_id(seed_id).screen_name

        plt.title('Local Followers Distribution for ' + seed_user + ' Global Threshold: ' + str(global_thresh) + ' Local Threshold: ' + str(local_thresh))
        plt.hist(counts, cumulative=-1, density=True, bins=range(0, max(counts) + 1, 1), histtype='stepfilled')
        plt.show()


    def global_attributes_of_deleted_users(self, seed_id: str, local_thresh, global_thresh):
        init_friends = self.friends_getter.get_user_friends_ids(seed_id)
        global_followers = []
        global_following = []
        global_tweets = []
        user_names = []

        friends = self.friends_cleaner.clean_friends_global(seed_id, init_friends, tweet_threshold=global_thresh,
                                                            follower_threshold=global_thresh, bot_threshold=0)
        clean_friends, deleted_friends = self.friends_cleaner.clean_friends_local(seed_id, friends, local_follower=0, local_following=local_thresh)

        deleted_users = self.user_getter.get_users_by_id_list(deleted_friends)

        titles = ['Distribution of Followers of Deleted Users at Local Threshold '
                  + str(local_thresh), 'Distribution of Following of Deleted Users at Local Threshold '
                  + str(local_thresh), 'Distribution of Tweets of Deleted Users at Local Threshold ' + str(local_thresh)]

        for user in deleted_users:
            global_followers.append(user.followers_count)
            global_following.append(user.friends_count)
            global_tweets.append(user.statuses_count)
            user_names.append(user.screen_name)

        title = titles[0]
        plt.bar(user_names, global_followers)
        plt.ylabel('Number of Followers')
        plt.xlabel('Deleted Users')
        plt.title(title)
        plt.show()

        title = titles[1]
        plt.bar(user_names, global_following)
        plt.ylabel('Number of Following')
        plt.xlabel('Deleted Users')
        plt.title(title)
        plt.show()

        title = titles[2]
        plt.bar(user_names, global_tweets)
        plt.ylabel('Number of Tweets')
        plt.xlabel('Deleted Users')
        plt.title(title)

        plt.show()

def jaccard_similarity(user_list1, user_list2):
    intersection = len(set(user_list1).intersection(set(user_list2)))
    union = (len(user_list1) + len(user_list2)) - intersection

    return float(intersection) / union

def overlap(user_list1, user_list2):
    intersection = len(set(user_list1).intersection(set(user_list2)))

    return float(intersection) / len(user_list1)
