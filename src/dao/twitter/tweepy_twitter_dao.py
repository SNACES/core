import datetime
from queue import Queue
from threading import Thread
import conf.credentials as credentials
from typing import Union, List, Dict
from tweepy import OAuthHandler, Stream, API, Cursor
from tweepy.streaming import StreamListener
from src.model.tweet import Tweet
from src.model.user import User
from src.dao.twitter.twitter_dao import TwitterGetter
from tweepy import TweepError
from src.shared.logger_factory import LoggerFactory
import threading

log = LoggerFactory.logger(__name__)


apiThreadLock = threading.Lock()
class BufferedUserTweetGetter():
    def __init__(self, num_tweets, subscriber, twitter_api, user_ids, q=Queue(), r=Queue()):
        self.twitter_api = twitter_api

        num_threads = 4
        self.q = q
        self.r = r

        self.limit = num_tweets
        self.subscriber = subscriber

        for user_id in user_ids:
            self.q.put(user_id)

        api_threads = []
        worker_threads = []

        # Api threads
        self.api_threads_running = num_threads
        for i in range(num_threads):
            t = Thread(target = self.stream_tweets)
            t.daemon = True
            api_threads.append(t)
            t.start()

        # Worker threads
        for i in range(num_threads):
            t = Thread(target = self.do_work)
            t.daemon = True
            worker_threads.append(t)
            t.start()

        self.api_threads = api_threads
        self.worker_threads = worker_threads

    def stream_tweets(self):
        while not self.q.empty():
            try:
                user_id = self.q.get(block=True, timeout=5)

                counter = 0
                try:
                    cursor = Cursor(self.twitter_api.user_timeline, user_id=user_id, count=200).items()
                    for data in cursor:
                        self.r.put(data)
                        counter += 1
                except TweepError as e:
                    log.error(e)

                log.info("Downloaded " + str(counter) + " Tweets for user " + str(user_id))
            except Exception as ex:
                # Exception is empty queue exception
                pass

        with apiThreadLock:
            self.api_threads_running -= 1

    def do_work(self):
        while self.api_threads_running != 0 or not self.r.empty():
            try:
                data = self.r.get(block=True, timeout=5)
                self.subscriber.on_status(data)
            except Exception as ex:
                # Exception is empty queue exception
                pass


class BufferedTweepyListener(StreamListener):
    def __init__(self, num_tweets, subscriber, q=Queue()):
        super().__init__()

        self.running = True

        num_threads = 4
        self.q = q

        threads = []
        for i in range(num_threads):
            t = Thread(target=self.do_work)
            t.daemon = True
            threads.append(t)
            t.start()

        self.counter = 0
        self.limit = num_tweets

        self.threads = threads

        self.subscriber = subscriber

    def on_status(self, data):
        self.q.put(data)
        self.counter += 1

        if self.counter < self.limit:
            return True
        else:
            self.running = False
            return False

    def get_data(self):
        while self.running or not self.q.empty():
            try:
                data = self.q.get(block=True, timeout=5)
                if data is not None:
                    self.subscriber.on_status(data)
            except Exception as ex:
                # Exception is empty exception
                pass

    def do_work(self):
        while self.running or not self.q.empty():
            try:
                data = self.q.get(block=True, timeout=5)
                if data is not None:
                    self.subscriber.on_status(data)
            except Exception as ex:
                # Exception is empty exception
                pass


class TweepyListener(StreamListener):
    def __init__(self, num_tweets, subscriber):
        super().__init__()

        self.counter = 0
        self.limit = num_tweets

        self.subscriber = subscriber

    def on_status(self, data):
        self.subscriber.on_status(data)
        self.counter += 1

        return self.counter < self.limit


class TwitterAuthenticator():
    def authenticate(self):
        auth = OAuthHandler(credentials.CONSUMER_KEY,
            credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN,
            credentials.ACCESS_TOKEN_SECRET)

        return auth


class TweepyTwitterGetter(TwitterGetter):
    def __init__(self):
        self.auth = TwitterAuthenticator().authenticate()
        self.twitter_api = API(self.auth, wait_on_rate_limit=True)

    def stream_tweets_by_user_id_list(self, user_ids, subscriber, num_tweets=0):
        getter = BufferedUserTweetGetter(num_tweets=num_tweets, subscriber=subscriber, user_ids=user_ids, twitter_api=self.twitter_api)

        api_threads = getter.api_threads
        for t in api_threads:
            t.join()

        log.info("All API threads joined, waiting for worker threads to store tweets")

        worker_threads = getter.worker_threads
        for t in worker_threads:
            t.join()

        log.info("Done streaming tweets")


    def buffered_stream_tweets(self, num_tweets, subscriber) -> None:
        listener = BufferedTweepyListener(num_tweets=num_tweets, subscriber=subscriber)

        stream = Stream(self.auth, listener)
        stream.filter(languages=["en"])
        stream.sample()

        threads = listener.threads
        for t in threads:
            t.join()

    def stream_tweets(self, num_tweets, subscriber) -> None:
        """
        Creates a twitter stream, which downloads the given number of tweets.
        Each time a tweet is downloaded, the subscriber is notified (their
        on_status method is called)

        @param num_tweets the number of tweers to download
        @param subscriber the object to notify each time a tweet is downloaded
        """
        listener = TweepyListener(num_tweets=num_tweets, subscriber=subscriber)

        stream = Stream(self.auth, listener)
        stream.filter(languages=["en"])
        stream.sample()

    def get_user_by_id(self, user_id: str) -> User:
        tweepy_user = self.twitter_api.get_user(user_id=user_id)

        if tweepy_user is not None:
            user = User.fromTweepyJSON(tweepy_user._json)
            return user

        return None

    def get_user_by_screen_name(self, screen_name: str) -> User:
        tweepy_user = self.twitter_api.get_user(screen_name=screen_name)

        if tweepy_user is not None:
            user = User.fromTweepyJSON(tweepy_user._json)
            return user

        return None

    def get_tweets_by_user_id(self, user_id, num_tweets=0):
        tweets = []
        try:
            cursor = Cursor(self.twitter_api.user_timeline, user_id=user_id, count=200).items(limit=num_tweets)
            for data in cursor:
                tweets.append(Tweet.fromTweepyJSON(data._json))
        except TweepError as e:
            log.error(e)

        return tweets

    def get_friends_ids_by_user_id(self, user_id: str, num_friends=0) -> List[str]:
        cursor = Cursor(self.twitter_api.friends_ids, user_id=user_id).items(limit=num_friends)

        friends_user_ids = []
        try:
            for id in cursor:
                friends_user_ids.append(id)
        except Exception as ex:
            log.error("Could not download friends ids")

        return user_id, friends_user_ids

    def get_friends_users_by_user_id(self, user_id: str, num_friends=0) -> List[User]:
        try:
            cursor = Cursor(self.twitter_api.friends, user_id=user_id).items(limit=num_friends)

            friends_users = []
            count = 0
            for tweepy_user in cursor:
                count += 1
                log.info("Downloaded user " + str(tweepy_user._json.get("id")))
                friends_users.append(User.fromTweepyJSON(tweepy_user._json))
            log.info("total friends {}".format(count))
        except Exception as e:
            log.error("error occurs")
        return user_id, friends_users

    def get_followers_ids_by_user_id(self, user_id: str, num_followers=0) -> List[User]:
        # TODO Catch error, and set ids to []
        cursor = Cursor(self.twitter_api.followers_id, user_id=user_id).items(limit=num_followers)

        followers_user_ids = []
        for id in cursor:
            followers_user_ids.append(id)

        return user_id, followers_user_ids

    def get_followers_users_by_user_id(self, user_id: str, num_followers=0) -> List[User]:
        cursor = Cursor(self.twitter_api.followers, user_id=user_id).items(limit=num_followers)

        followers_users = []
        for follower_user in cursor:
            follower_users.append(User.fromTweepyJSON(follower_user))

        return user_id, followers_users
