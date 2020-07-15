from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
from typing import Union
from datastore import *
import datetime
import credentials

from tweepy.streaming import StreamListener
from tweepy import Stream

class TweepyListener(StreamListener):
    def __init__(self, num_tweets):
        super().__init__()
        self.counter = 0
        self.limit = num_tweets
        self.tweets = []

    # TODO:
    def on_status(self, data):
        try:
            # userid = status.user.id_str
            # print(data)
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


class TweepyDAO(InputDAO):
    def __init__(self):
        self.auth = TwitterAuthenticator().authenticate()
        self.twitter_api = API(self.auth, wait_on_rate_limit=True)

    def get_tweets_by_timeframe_user(self, id, start_date, end_date, num_tweets):
        total_tweets = Cursor(self.twitter_api.user_timeline, id=id).items(num_tweets)
        def pred(tweet):
                is_correct_date = tweet.created_at > start_date and tweet.created_at < end_date
                is_correct_user = tweet.user.id == id or tweet.user.screen_name == id
                return is_correct_date and is_correct_user

        tweet_objects = list(filter(pred, total_tweets))
        json_tweets = list(map(lambda t: t._json, tweet_objects))
        return json_tweets

    def get_tweets_by_user(self, id, num_tweets):
        total_tweets = Cursor(self.twitter_api.user_timeline, id=id).items(num_tweets)
        json_tweets = list(map(lambda t: t._json, total_tweets))
        
        return json_tweets
    
    def get_random_tweets(self):
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
    
    def get_friends_by_screen_name(self, screen_name, num_friends):
        friends = Cursor(self.twitter_api.friends_ids, screen_name=screen_name).items(num_friends)
        friends_ids = [friend_id for friend_id in friends]

        return [self.twitter_api.get_user(user_id=friend_id).screen_name for friend_id in friends_ids]

    def get_friends_by_id(self, id, num_friends):
        return [friend_id for friend_id in Cursor(self.twitter_api.friends_ids, user_id=id).items(num_friends)]
    
    def get_following_by_screen_name(self, screen_name, num_following):
        following_users_id = [following_id for following_id in Cursor(self.twitter_api.followers_ids, screen_name=screen_name).items(num_following)]

        return [self.twitter_api.get_user(user_id=following_id).screen_name for following_id in following_users_id]
    
    def get_following_by_id(self, id, num_following):
        return [following_id for following_id in Cursor(self.twitter_api.followers_ids, user_id=id).items(num_following)]
    


# def read(self, query):
#         query_type = query["query_type"]

#         if (query_type == "get_tweets_by_timeframe_user"):
#             id = query["id"]
#             start_date = query["start_date"]
#             end_date = query["end_date"]
#             num_tweets = query["num_tweets"]
#             total_tweets = Cursor(self.twitter_api.user_timeline, id=id).items(num_tweets)

#             def pred(tweet):
#                 is_correct_date = tweet.created_at > start_date and tweet.created_at < end_date
#                 is_correct_user = tweet.user.id == id or tweet.user.screen_name == id
#                 return is_correct_date and is_correct_user

#             tweet_objects = list(filter(pred, total_tweets))
#             json_tweets = list(map(lambda t: t._json, tweet_objects))
#             return json_tweets
#         elif (query_type == "get_tweets_user"):
#             id = query["id"]
#             num_tweets = query["num_tweets"]
#             total_tweets = Cursor(self.twitter_api.user_timeline, id=id).items(num_tweets)
#             json_tweets = list(map(lambda t: t._json, total_tweets))
#             return json_tweets
#         elif (query_type == "get_random_tweets"):
#             listener = TweepyListener(1)

#             stream = Stream(self.auth, listener)
#             # filter out all non-English Tweets
#             stream.filter(languages=["en"]) 
#             stream.sample()
            
#             random_tweet = listener.tweets[0] if len(listener.tweets) != 0 else None
#             if random_tweet != None:
#                 json_tweet = random_tweet._json 
#                 # list(map(lambda t: t._json, random_tweets))   
#                 return json_tweet

#             return None
#         elif (query_type == "get_friends_by_screen_name"):
#             screen_name = query["screen_name"]
#             num_friends = query["num_friends"]
#             friends = Cursor(self.twitter_api.friends_ids, screen_name=screen_name).items(num_friends)
#             friends_ids = [friend_id for friend_id in friends]

#             return [self.twitter_api.get_user(user_id=friend_id).screen_name for friend_id in friends_ids]
#         elif (query_type == "get_friends_by_id"):
#             id = query["id"]
#             num_friends = query["num_friends"]
            
#             return [friend_id for friend_id in Cursor(self.twitter_api.friends_ids, user_id=id).items(num_friends)]
#         elif (query_type == "get_following_by_screen_name"):
#             screen_name = query["screen_name"]
#             num_following = query["num_following"]

#             following_users_id = [following_id for following_id in Cursor(self.twitter_api.followers_ids, screen_name=screen_name).items(num_following)]

#             return [self.twitter_api.get_user(user_id=following_id).screen_name for following_id in following_users_id]
#         elif (query_type == "get_following_by_id"):
#             id = query["id"]
#             num_following = query["num_following"]

#             return [following_id for following_id in Cursor(self.twitter_api.followers_ids, user_id=id).items(num_following)]
#         else:
#             raise Exception("Invalid Query")