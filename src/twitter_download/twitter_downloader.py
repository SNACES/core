import functools
import datetime
import functools
from typing import Union, List

from src.general.process import Process

"""
Download Tweets for use in future algorithms.
"""
class TwitterTweetDownloader(Process):
    def __init__(self, init_path, input_DAOs={}, output_DAOs={}):
        Process.__init__(self, init_path, input_DAOs, output_DAOs)

    def get_tweets_by_timeframe_user(self, id: Union[str, int], start_date: datetime,
                                     end_date: datetime, num_tweets: int, input_name: str, output_name: str):
        """
        Return num_tweets tweets made by user with id(username or user id) id between start_date and end_date.
        """

        tweets = self.input_DAOs[input_name].get_tweets_by_timeframe_user(
            id, start_date, end_date, num_tweets)
        self.output_DAOs[output_name].store_tweet_by_timeframe_user(
            id, start_date, end_date, tweets)

    def get_tweets_by_user(self, id: Union[str, int], num_tweets: int, input_name: str, output_name: str) -> list:
        tweets = self.input_DAOs[input_name].get_tweets_by_user(id, num_tweets)
        self.output_DAOs[output_name].store_tweet_by_user(id, tweets)

    def get_random_tweet(self, input_name: str, output_name: str):
        tweet = self.input_DAOs[input_name].get_random_tweet()
        self.output_DAOs[output_name].store_random_tweet(tweet)

        return tweet


"""
Download Twitter Friends for use in future algorithms.
"""


class TwitterFriendsDownloader(Process):
    def __init__(self, init_path, input_DAOs={}, output_DAOs={}):
        Process.__init__(self, init_path, input_DAOs, output_DAOs)

    def get_friends_by_screen_name(self, screen_name: str, num_friends: int, input_name: str, output_name: str) -> list:
        """
        Return a list of screen_names of friends of user with screen name screen_name.
        """

        assert type(screen_name) == str

        friends = self.input_DAOs['TweepyClient'].get_friends_by_screen_name(
            screen_name, num_friends)
        self.output_DAOs["getFriendsByScreenName"].store_friends_by_screen_name(
            screen_name, friends)

        return friends

    def get_friends_by_id(self, id: int, num_friends: int, input_name: str, output_name: str) -> list:
        """
        Return a list of ids of friends of user with id id.
        """

        assert type(id) == int

        friends = self.input_DAOs['TweepyClient'].get_friends_by_id(
            id, num_friends)
        self.output_DAOs["getFriendsByID"].store_friends_by_id(id, friends)


"""
Download Twitter Following for use in future algorithms.
"""


class TwitterFollowingDownloader(Process):
    def __init__(self, init_path, input_DAOs={}, output_DAOs={}):
        Process.__init__(self, init_path, input_DAOs, output_DAOs)

    def get_following_by_screen_name(self, screen_name: str, num_following: int, input_name: str, output_name: str) -> list:
        assert type(screen_name) == str

        following_users_screen_name = self.input_DAOs[input_name].get_following_by_screen_name(
            screen_name, num_following)
        self.output_DAOs[output_name].store_following_by_screen_name(
            screen_name, following_users_screen_name)

    def get_following_by_id(self, id: int, num_following: int, input_name: str, output_name: str) -> list:
        assert type(id) == int

        following_users_ID = self.input_DAOs[input_name].get_following_by_id(
            id, num_following)
        self.output_DAOs[output_name].store_following_by_id(
            id, following_users_ID)


def rate_limited_functions() -> str:
    functions_list = ["get_user_tweets_by_screen_name", "get_user_tweets_by_id",
                      "get_friends_screen_names_by_screen_name", "get_friends_ids_by_id"]

    result = ""
    for function_name in functions_list:
        result += function_name + "\n"
    return result.strip()


# def filter_out_bots(users: List[str], start: datetime, end: datetime, threshold=0.75) -> List[str]:
#     """
#     Filters out bots from the supplied list of screen names. An account is flagged as a bot
#     if more than the given threshold of total tweets supplied by the account in the given
#     timeframe are retweets.
#     """
#     li = []
#     for user in users:
#         retweets, tweets = self.get_tweets(user, start, end)
#         if len(retweets) + len(tweets) > 0 and (len(retweets)/(len(tweets)+len(retweets)) <= 0.75):
#             li.append(user)

#     return li


class UserListProcessor:
    """
    Return a list of users given the path to a file containing a list of users.
    """

    def user_list_parser(self, user_list_file_path):
        with open(user_list_file_path, 'r') as stream:
            return [user.strip() for user in stream]

    """
    Precondition: argv matches the args for download_function
    """

    def download_function_by_user_list(self, download_function, user_list, *argv):
        def curried_operation(acc, id): return download_function(
            id, *argv)  # acc is a dummy var

        self.process_user_list(user_list, curried_operation)

    def process_user_list(self, user_list, curried_function):
        functools.reduce(curried_function, user_list)


if __name__ == "__main__":
    start_date = datetime.datetime(2019, 6, 1, 0, 0, 0)
    end_date = datetime.datetime(2020, 5, 7, 0, 0, 0)

    import os
    # note that we need to pass in full path
    ds_config_path = os.getcwd() + "/../General/ds-init-config.yaml"

    num_tweets_to_download = 1
    twitter_downloader = TwitterTweetDownloader(ds_config_path)
    friends_downloader = TwitterFriendsDownloader(ds_config_path)
    following_downloader = TwitterFollowingDownloader(ds_config_path)

    id = "animesh_garg"
    twitter_downloader.get_tweets_by_timeframe_user(id, start_date, end_date, num_tweets_to_download, 'TweepyClient', 'getTweetsByTimeframeUser')
    # friends_downloader.get_friends_by_screen_name(id, 1, 'TweepyClient', 'getFriendsByScreenName')
    # following_downloader.get_following_by_screen_name(id, 1, 'TweepyClient', 'getFollowingByScreenName')

    # "mongodb://localhost:2223"
