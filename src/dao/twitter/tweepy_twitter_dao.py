import datetime
from queue import Queue
from threading import Thread
import conf.credentials as credentials
from typing import Union, List, Dict
from tweepy import OAuthHandler, Stream, API, Cursor
from tweepy.streaming import StreamListener
from src.model.tweet import Tweet
from src.model.user import User

class BufferedTweepyListener(StreamListener):
    def __init__(self, num_tweets, subscriber, q = Queue()):
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

    def do_work(self):
        while self.running:
            try:
                data = self.q.get(block=True, timeout=5)
                if data is not None:
                    self.subscriber.on_status(data)
            except Exception as e:
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

class TweepyTwitterGetter():
    def __init__(self):
        self.auth = TwitterAuthenticator().authenticate()
        self.twitter_api = API(self.auth, wait_on_rate_limit=True)

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

    def get_tweets_by_screen_name(self, screen_name: str, num_tweets=0):
        user = self.get_user_by_screen_name(screen_name)

        return self.get_tweets_by_user_id(user.id)

    def get_tweets_by_user_id(self, user_id, num_tweets=0):
        tweets = [Tweet.fromTweepyJSON(data._json)
            for data
            in Cursor(self.twitter_api.user_timeline, user_id=user_id).items(limit=num_tweets)]

        return tweets

    def get_user_by_id(self, user_id: str) -> User:
        tweepy_user = self.twitter_api.get_user(user_id=user_id)

        if tweepy_user is not None:
            user = User.fromTweepyJSON(tweepy_user._json)
            return user

        return None

    def get_users_by_user_id_list(self, user_id_list: List[str]) -> List[User]:
        return [self.get_users_by_id(user_id) for user_id in user_id_list]

    def get_user_by_screen_name(self, screen_name: str) -> User:
        tweepy_user = self.twitter_api.get_user(screen_name=screen_name)

        if tweepy_user is not None:
            user = User.fromTweepyJSON(tweepy_user._json)
            return user

        return None

    def get_friends_users_by_screen_name(self, screen_name: str, num_friends=0) -> List[User]:
        user = self.get_user_by_screen_name(screen_name)

        return self.get_friends_users_by_user_id(user.id, num_friends=num_friends)

    def get_friends_users_by_user_id(self, user_id: str, num_friends=0) -> List[User]:
        friends_tweepy_users = [user for user in Cursor(self.twitter_api.friends, user_id=user_id).items(limit=num_friends)]
        friends_users = [User.fromTweepyJSON(tweepy_user._json) for tweepy_user in friends_tweepy_users]

        return user_id, friends_users

    def get_friends_ids_by_screen_name(self, screen_name: str, num_friends=0) -> List[str]:
        user = self.get_user_by_screen_name(screen_name)
        return self.get_friends_ids_by_user_id(user.id, num_friends=num_friends)

    def get_friends_ids_by_user_id(self, user_id: str, num_friends=0) -> List[str]:
        friends_user_ids = [follower_id for follower_id in Cursor(self.twitter_api.friends_ids, user_id=user_id).items(limit=num_friends)]

        return user_id, friends_user_ids

    def get_followers_ids_by_id(self, user_id: str, num_followers=0) -> List[User]:
        followers_user_ids = [friend_id for friend_id in Cursor(self.twitter_api.followers_id, user_id=user_id).items(limit=num_followers)]

        return user_id, followers_user_ids

    def get_followers_ids_by_screen_name(self, screen_name: str, num_followers=0) -> List[User]:
        user = self.get_user_by_screen_name(screen_name)
        return self.get_followers_by_id(user.id, num_followers=num_followers)
