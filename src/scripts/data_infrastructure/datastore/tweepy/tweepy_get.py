import datetime
import conf.credentials as credentials

from typing import Union
from tweepy import OAuthHandler, Stream, API, Cursor
from tweepy.streaming import StreamListener

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


class TweepyGetDAO():
    def __init__(self):
        self.auth = TwitterAuthenticator().authenticate()
        self.twitter_api = API(self.auth, wait_on_rate_limit=True)

    def get_tweets_by_user(self, id, num_tweets=None, start_date=None, end_date=None):
        """
        Precondition: if a start_date is provided, then so must end_date(and vice versa)
        """

        if num_tweets is None:
            total_tweets = Cursor(self.twitter_api.user_timeline, id=id).items()
        else:
            total_tweets = Cursor(self.twitter_api.user_timeline, id=id).items(num_tweets) 
        
        def pred(tweet):
            is_correct_date = tweet.created_at >= start_date and tweet.created_at < end_date
            is_correct_user = tweet.user.id == id or tweet.user.screen_name == id
            return is_correct_date and is_correct_user
        
        total_tweets = list(filter(pred, total_tweets)) if start_date and end_date else list(total_tweets)

        retweets = list(filter(lambda t: 'retweeted_status' in t._json, total_tweets))
        json_retweets = list(map(lambda t: t._json, retweets))

        tweets = list(filter(lambda t: 'retweeted_status' not in t._json, total_tweets))
        json_tweets = list(map(lambda t: t._json, tweets))
        
        return json_tweets, json_retweets
    
    def get_random_tweet(self):
        listener = TweepyListener(1)

        stream = Stream(self.auth, listener)
        # filter out all non-English Tweets
        stream.filter(languages=["en"]) 
        stream.sample()
        
        random_tweet = listener.tweets[0] if len(listener.tweets) != 0 else None
        if random_tweet != None:
            json_tweet = random_tweet._json 
            # list(map(lambda t: t._json, random_tweets))   
            return json_tweet

        return None
    
    def get_friends_by_screen_name(self, screen_name, num_friends=None):
        if num_friends is None:
             friends = Cursor(self.twitter_api.friends_ids, screen_name=screen_name).items() 
        else:
            friends = Cursor(self.twitter_api.friends_ids, screen_name=screen_name).items(num_friends) 
        
        friends_ids = [friend_id for friend_id in friends]

        return [self.twitter_api.get_user(user_id=friend_id).screen_name for friend_id in friends_ids]

    def get_friends_by_id(self, id, num_friends=None):
        if num_friends is None:
            [friend_id for friend_id in Cursor(self.twitter_api.friends_ids, user_id=id).items()]
        else:
            return [friend_id for friend_id in Cursor(self.twitter_api.friends_ids, user_id=id).items(num_friends)]
    
    def get_followers_by_screen_name(self, screen_name, num_followers=None):
        if num_followers is None:
            followers_users_id = [followers_id for followers_id in Cursor(self.twitter_api.followers_ids, screen_name=screen_name).items()]
        else:
            followers_users_id = [followers_id for followers_id in Cursor(self.twitter_api.followers_ids, screen_name=screen_name).items(num_followers)]

        return [self.twitter_api.get_user(user_id=followers_id).screen_name for followers_id in followers_users_id]
    
    def get_followers_by_id(self, id, num_followers=None):
        if num_followers is None:     
            return [followers_id for followers_id in Cursor(self.twitter_api.followers_ids, user_id=id).items()]
        else: 
            return [followers_id for followers_id in Cursor(self.twitter_api.followers_ids, user_id=id).items(num_followers)]