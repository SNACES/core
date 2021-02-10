from typing import Union, List
from src.model.tweet import Tweet
from src.model.user import User
from src.dao.twitter.twitter_dao import TwitterGetter
from src.dao.raw_tweet.setter.raw_tweet_setter import RawTweetSetter
from src.shared.logger_factory import LoggerFactory

log = LoggerFactory.logger(__name__)


class UserTweetDownloader():
    """
    Downloads tweets for a particular user
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
        log.info("Downloaded " + str(len(tweets)) + " Tweets for user " + str(user_id))
        self.raw_tweet_setter.store_tweets(tweets)

    def download_user_tweets_by_user_list(self, user_ids: List[str]):
        num_ids = len(user_ids)
        count = 0
        for id in user_ids:
            self.download_user_tweets_by_user_id(id)

            count += 1

            log.log_progress(log, count, num_ids)

        log.info("Done downloading for user list")

    def stream_tweets_by_user_list(self, user_ids: List[str]):
        subscriber = self.Subscriber(self.raw_tweet_setter)
        try:
            self.twitter_getter.stream_tweets_by_user_id_list(user_ids, subscriber)
        except Exception as e:
            raise e

    class Subscriber():
        def __init__(self, raw_tweet_setter: RawTweetSetter):
            self.raw_tweet_setter = raw_tweet_setter

        def on_status(self, data):
            tweet = Tweet.fromTweepyJSON(data._json)
            self.raw_tweet_setter.store_tweet(tweet)
