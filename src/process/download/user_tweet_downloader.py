from typing import Union, List
from src.model.tweet import Tweet
from src.model.user import User
from src.dao.twitter.twitter_dao import TwitterGetter
from src.dao.raw_tweet.setter.raw_tweet_setter import RawTweetSetter

class UserTweetDownloader():
    """
    Downloads tweets fow a particular user
    """

    def __init__(self, twitter_getter: TwitterGetter, raw_tweet_setter: RawTweetSetter):
        self.twitter_getter = twitter_getter
        self.raw_tweet_setter = raw_tweet_setter

    def download_user_tweets_by_user(self, user: User) -> None:
        self.download_user_tweets_by_user_id(user.id)

    def download_user_tweets_by_screen_name(self, screen_name: str) -> None:
        tweets = self.twitter_getter.get_tweets_by_screen_name(screen_name)
        self.raw_tweet_setter.store_tweets(tweets)

    def download_user_tweets_by_user_id(self, user_id: str) -> None:
        tweets = self.twitter_getter.get_tweets_by_user_id(user_id)
        self.raw_tweet_setter.store_tweets(tweets)
