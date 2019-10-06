from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
from typing import Union

import datetime
import credentials

class TwitterAuthenticator():
    def authenticate(self):
        auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
        
        return auth

"""
Client that interacts with the Tweepy API
"""
class TwitterDataPreprocessor():
    def __init__(self, screen_name = None):
        self.auth = TwitterAuthenticator().authenticate()
        self.twitter_api = API(self.auth)
 
    def get_tweets(self, id: Union[str, int], start_date: datetime,
                   end_date: datetime, num_tweets: int) -> list:
        """
        Return num_tweets tweets made by user with id(username or user id) id between start_date and end_date.
        """
        
        total_tweets = Cursor(self.twitter_api.user_timeline, id=id).items(num_tweets)
        def pred(tweet):
            is_correct_date = tweet.created_at > start_date and tweet.created_at < end_date
            is_correct_user = tweet.user.id == id or tweet.user.screen_name == id
            return is_correct_date and is_correct_user

        return list(filter(pred, total_tweets))
        
    def get_friends_by_screen_name(self, screen_name: str, num_friends) -> list:
        """  
        Return a list of screen_names of friends of user with screen name screen_name.
        """
        
        assert type(screen_name) == str

        friends_ids = [friend_id for friend_id in Cursor(self.twitter_api.friends_ids, 
                                                         screen_name=screen_name).items(num_friends)]

        return [self.twitter_api.get_user(user_id=friend_id).screen_name for friend_id in friends_ids]
    
    def get_friends_by_id(self, id: int, num_friends) -> list:
        """  
        Return a list of ids of friends of user with id id.
        """
        
        assert type(id) == int
        
        return [friend_id for friend_id in Cursor(self.twitter_api.friends_ids, user_id=id).items(num_friends)]
       
    def rate_limited_functions(self) -> str:
        functions_list = ["get_user_tweets_by_screen_name", "get_user_tweets_by_id", 
                          "get_friends_screen_names_by_screen_name", "get_friends_ids_by_id"]
        
        result = ""
        for function_name in functions_list:
            result += function_name + "\n"

        return result.strip()


if __name__ == "__main__":
    twitter_client = TwitterDataPreprocessor()

    start_date = datetime.datetime(2019, 6, 1, 0, 0, 0)
    end_date =   datetime.datetime(2019, 10, 7, 0, 0, 0)

    tweets = twitter_client.get_tweets("realDonaldTrump", start_date, end_date, 1)

    # print(tweets)

    # print(twitter_client.get_friends_by_id(1174436690078752768, 5))

    # print(twitter_client.print_rate_limited_functions())