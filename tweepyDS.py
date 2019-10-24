from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
from typing import Union
from datastore import DataStore
import datetime
import credentials

class TwitterAuthenticator():
    def authenticate(self):
        auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
        
        return auth


class TweepyDS(DataStore):
    def __init__(self):
        self.auth = TwitterAuthenticator().authenticate()
        self.twitter_api = API(self.auth)

    def read(self, query):
        query_type = query["query_type"]

        if (query_type == "get_tweets"):
            id = query["id"]
            start_date = query["start_date"]
            end_date = query["end_date"]
            num_tweets = query["num_tweets"]
            total_tweets = Cursor(self.twitter_api.user_timeline, id=id).items(num_tweets)

            def pred(tweet):
                is_correct_date = tweet.created_at > start_date and tweet.created_at < end_date
                is_correct_user = tweet.user.id == id or tweet.user.screen_name == id
                return is_correct_date and is_correct_user

            tweet_objects = list(filter(pred, total_tweets))
            json_tweets = list(map(lambda t: t._json, tweet_objects))
            return json_tweets

        elif (query_type == "get_friends_by_screen_name"):
            screen_name = query["screen_name"]
            num_friends = query["num_friends"]
            friends = Cursor(self.twitter_api.friends_ids, screen_name=screen_name).items(num_friends)
            friends_ids = [friend_id for friend_id in friends]

            return [self.twitter_api.get_user(user_id=friend_id).screen_name for friend_id in friends_ids]
        elif (query_type == "get_friends_by_id"):
            id = query["id"]
            num_friends = query["num_friends"]
            
            return [friend_id for friend_id in Cursor(self.twitter_api.friends_ids, user_id=id).items(num_friends)]
        else:
            raise Exception("Invalid Query")



