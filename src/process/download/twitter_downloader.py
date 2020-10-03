import functools
import datetime

from typing import Union, List
from src.model.raw_tweet import RawTweet

class TwitterTweetDownloader():
    """
    Download Tweets for use in future algorithms.
    """

    def gen_user_tweets(self, id: Union[str, int], tweepy_getter, tweet_setter, num_tweets=None, start_date=None, end_date=None) -> List[RawTweet]:
        """
        Retrieves tweets from twitter from a given user, and stores them

        @param id the id or username of the user
        @param tweepy_getter the dao to retrieve tweets from tweepy
        @param tweept_setter the dao to store tweets with
        @param num_tweets the number of tweets to retrieve
        @param start_date - Optional, the earliest date to pull tweets from
        @param end_date - Optional, the end date to pull tweets from

        @return a list of Tweets
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

    def gen_random_tweet(self, tweepy_getter, tweet_setter) -> RawTweet:
        """
        Retrieves a random tweet from Twitter

        @param tweepy_getter the dao to retrieve tweets from tweepy
        @param tweet_setter the dao to store the raw tweet in

        @return the random tweet
        """
        tweet = tweepy_getter.get_random_tweet()
        tweet_setter.store_random_tweet(tweet)

        return tweet

class TwitterFriendsDownloader():
    """
    Download Twitter Friends for use in future algorithms.
    """
    def gen_friends_by_screen_name(self, screen_name: str, tweepy_getter, user_friends_setter, num_friends=None) -> List[str]:
        """
        Retrieves a list of screen_names of friends for the user with the given screen name

        @param screen_name the screen name of the user to query on
        @param tweepy_getter the getter to access twitter with
        @param user_friends_setter the dao to store the output
        @param num_friends Optional - if specified, the maximum number of friends to retrieve

        @return a list of screen names of users
        """

        assert type(screen_name) == str

        friends = tweepy_getter.get_friends_by_screen_name(screen_name, num_friends)
        user_friends_setter.store_friends_by_screen_name(screen_name, friends)

        return friends

    def gen_friends_by_id(self, id: int, tweepy_getter, user_friends_setter, num_friends=None) -> List[int]:
        """
        Retrieves a list of ids of friends for the user with the given id

        @param id the id of the user to query on
        @param tweepy_getter the getter to access twitter with
        @param user_friends_setter the dao to store the output in
        @param num_friends Optional - if specified, the maximum number of friends to retreive

        @return a list of ids of users friends with the given user
        """

        assert type(id) == int

        friends = tweepy_getter.get_friends_by_id(id, num_friends)
        user_friends_setter.store_friends_by_id(id, friends)

    def gen_user_local_neighborhood(self, user: str, tweepy_getter, user_friends_getter, user_friends_setter):
        """
        Gets and stores friends, as well as friends of friends for a given user

        @param user the screen name of the user to build the network for
        @param tweepy_getter the dao to access twitter with
        @param user_friends_getter the dao to access the given users friends with
        @param user_friends_setter the dao to store the local network in
        """
        user_friends_list = user_friends_getter.get_friends_by_name(user)
        if not user_friends_list:
            user_friends_list = self.gen_friends_by_screen_name(user, tweepy_getter, user_friends_setter, 5)

        for friend in user_friends_list:
            friend_friends_list = user_friends_getter.get_friends_by_name(friend)
            if not friend_friends_list:
                self.gen_friends_by_screen_name(friend, tweepy_getter, user_friends_setter, 5)

class TwitterFollowersDownloader():
    """
    Download Twitter Followers for use in future algorithms.
    """
    
    def gen_followers_by_screen_name(self, screen_name: str, tweepy_getter, user_followers_setter, num_followers=None) -> List[str]:
        """
        Gets a list of followers of a user by screen name

        @param screen_name the screen name of the user to search for
        @param tweepy_getter the dao to access twitter with
        @param user_followers_setter the dao to store the users followers in
        @param num_followers the maximum number of followers to retrieve

        @return a list of screen names of followers for the given user
        """
        assert type(screen_name) == str

        followers_users_screen_name = tweepy_getter.get_followers_by_screen_name(screen_name, num_followers)
        user_followers_setter.store_followers_by_screen_name(screen_name, followers_users_screen_name)

    def gen_followers_by_id(self, id: int, tweepy_getter, user_followers_setter, num_followers=None) -> List[int]:
        """
        Gets a list of followers of a user by id

        @param id the id of the user to query on
        @param tweepy_getter the dao to access twitter with
        @param user_followers_setter the dao to store twitter followers in
        @param num_followers the maximum number of followers to retrieve

        @return a list of ids of followers for the given user
        """
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
