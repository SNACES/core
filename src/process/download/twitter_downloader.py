import functools
import datetime

from typing import Union, List

"""
Download Tweets for use in future algorithms.
"""
class TwitterTweetDownloader():
    def gen_user_tweets(self, id: Union[str, int], tweepy_getter, tweet_setter, num_tweets=None, start_date=None, end_date=None) -> list:
        """
        Return num_tweets tweets/retweets made by user with id(username or user id) id.
        """
        if start_date and end_date:
            tweets, retweets = tweepy_getter.get_tweets_by_user(id, num_tweets, start_date, end_date)
        elif start_date or end_date:
            raise Exception("Please provide valid start and end dates")
        else:
            tweets, retweets = tweepy_getter.get_tweets_by_user(id, num_tweets)
        tweet_setter.store_tweet_by_user(id, tweets, retweets)

    # def gen_user_tweets_in_timeframe(self, id: Union[str, int], start_date: datetime,
    #                                  end_date: datetime, get_dao, set_dao, num_tweets=None):
    #     """
    #     Return num_tweets tweets/retweets made by user with id(username or user id) id between start_date and end_date.
    #     """

    #     tweets, retweets = get_dao.get_tweets_by_timeframe_user(id, start_date, end_date, num_tweets)
    #     set_dao.store_tweet_by_user(id, tweets, retweets)
    
    def gen_random_tweet(self, tweepy_getter, tweet_setter):
        tweet = tweepy_getter.get_random_tweet()
        tweet_setter.store_random_tweet(tweet)

        return tweet


"""
Download Twitter Friends for use in future algorithms.
"""
class TwitterFriendsDownloader():
    def gen_friends_by_screen_name(self, screen_name: str, tweepy_getter, user_friends_setter, num_friends=None) -> list:
        """
        Return a list of screen_names of friends of user with screen name screen_name.
        """

        assert type(screen_name) == str

        friends = tweepy_getter.get_friends_by_screen_name(screen_name, num_friends)
        user_friends_setter.store_friends_by_screen_name(screen_name, friends)

        return friends

    def gen_friends_by_id(self, id: int, tweepy_getter, user_friends_setter, num_friends=None) -> list:
        """
        Return a list of ids of friends of user with id id.
        """

        assert type(id) == int

        friends = tweepy_getter.get_friends_by_id(id, num_friends)
        user_friends_setter.store_friends_by_id(id, friends)

    # Implementation using tweepy - slow, API-constrained
    def gen_user_local_neighborhood(self, user: str, tweepy_getter, user_friends_getter, user_friends_setter):
        """
        Note that user refers to screen name.
        """
        user_friends_list = user_friends_getter.get_friends_by_name(user)
        if not user_friends_list:
            user_friends_list = self.gen_friends_by_screen_name(user, tweepy_getter, user_friends_setter)

        for friend in user_friends_list:
            friend_friends_list = user_friends_getter.get_friends_by_name(friend)
            if not friend_friends_list:
                self.gen_friends_by_screen_name(friend, tweepy_getter, user_friends_setter)


"""
Download Twitter Followers for use in future algorithms.
"""
class TwitterFollowersDownloader():
    def gen_followers_by_screen_name(self, screen_name: str, tweepy_getter, user_followers_setter, num_followers=None) -> list:
        assert type(screen_name) == str

        followers_users_screen_name = tweepy_getter.get_followers_by_screen_name(screen_name, num_followers)
        user_followers_setter.store_followers_by_screen_name(screen_name, followers_users_screen_name)

    def gen_followers_by_id(self, id: int, tweepy_getter, user_followers_setter, num_followers=None) -> list:
        assert type(id) == int

        followers_users_ID = tweepy_getter.get_followers_by_id(id, num_followers)
        user_followers_setter.store_followers_by_id(id, followers_users_ID)


# def rate_limited_functions() -> str:
#     functions_list = ["get_user_tweets_by_screen_name", "get_user_tweets_by_id",
#                       "get_friends_screen_names_by_screen_name", "get_friends_ids_by_id"]

#     result = ""
#     for function_name in functions_list:
#         result += function_name + "\n"
#     return result.strip()


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
