import datetime
import conf.credentials as credentials

from typing import Union
from tweepy import OAuthHandler, Stream, API, Cursor
from tweepy.streaming import StreamListener
from src.model.tweet import Tweet

class TweepyListener(StreamListener):
    def __init__(self, num_tweets):
        super().__init__()
        self.counter = 0
        self.limit = num_tweets
        self.tweets = []

    def on_status(self, data):
        try:
            self.tweets.append(data)
            self.counter += 1
            if self.counter < self.limit:
                return True
            else:
                return False
        except BaseException as e:
            print('failed on_status,',str(e))


class TwitterAuthenticator():
    def authenticate(self):
        auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)

        return auth


class TweepyTwitterGetter():
    def __init__(self):
        self.auth = TwitterAuthenticator().authenticate()
        self.twitter_api = API(self.auth, wait_on_rate_limit=True)

    def get_random_tweet(self):
        listener = TweepyListener(1)

        stream = Stream(self.auth, listener)
        # filter out all non-English Tweets
        stream.filter(languages=["en"])
        stream.sample()

        random_tweet = listener.tweets[0] if len(listener.tweets) != 0 else None
        if random_tweet != None:
            tweet = Tweet.fromTweepyJSON(random_tweet._json)
            return tweet

        return None
