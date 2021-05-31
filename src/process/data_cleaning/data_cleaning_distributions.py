import matplotlib.pyplot as plt
import numpy as np
from src.dao.user_friend.getter.friend_getter import FriendGetter
from src.dao.user.getter.user_getter import UserGetter
from src.shared.logger_factory import LoggerFactory

log = LoggerFactory.logger(__name__)

class DataCleaningDistributions():
    """
    Given a seed user, creates distributions of number of tweets, followers, etc
    of the users in the local neighborhood
    """
    def __init__(self, friends_getter: FriendGetter, user_getter: UserGetter):
        self.friends_getter = friends_getter
        self.user_getter = user_getter

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

