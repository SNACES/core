from typing import Union
from algorithm import Algorithm

import datetime

"""
Preprocess Tweepy data for use in future algorithms.
"""
class TwitterDownloader(Algorithm):
    def __init__(self, init_path, input_datastores={}, output_datastores={}):
        Algorithm.__init__(self, init_path, input_datastores, output_datastores)
        
    def get_tweets(self, id: Union[str, int], start_date: datetime,
                   end_date: datetime, num_tweets: int) -> list:
        """
        Return num_tweets tweets made by user with id(username or user id) id between start_date and end_date.
        """
        
        query = {"query_type": "get_tweets",
                 "id": id, 
                 "start_date": start_date, 
                 "end_date": end_date, 
                 "num_tweets": num_tweets
                 }

        tweets = self.input_datastores['TweepyClient'].read(query) 
        document = {
            "id": id,
            "start_date": start_date,
            "end_date": end_date,
            # "num_tweets": num_tweets
            "tweets": tweets
        }
        self.output_datastores['TwitterDownload'].create("getTweets", document)
    
    def get_friends_by_screen_name(self, screen_name: str, num_friends: int) -> list:
        """  
        Return a list of screen_names of friends of user with screen name screen_name.
        """
        
        assert type(screen_name) == str

        query = {"query_type": "get_friends_by_screen_name", 
                 "screen_name": screen_name,
                 "num_friends": num_friends}
        
        friends = self.input_datastores['TweepyClient'].read(query)
        document = {
            "screen_name": screen_name,
            # "num_friends": num_friends,
            "friends": friends
        }
        self.output_datastores['TwitterDownload'].create("getFriendsByScreenName", document)
    
    def get_friends_by_id(self, id: int, num_friends: int) -> list:
        """  
        Return a list of ids of friends of user with id id.
        """
        
        assert type(id) == int
        
        query = {"query_type": "get_friends_by_id", 
                 "id": id,
                 "num_friends": num_friends}

        friends = self.input_datastores['TweepyClient'].read(query)
        document = {
            "id": id,
            # "num_friends": num_friends,
            "friends": friends
        }
        self.output_datastores['TwitterDownload'].create("getFriendsByID", document)

    def rate_limited_functions(self) -> str:
        functions_list = ["get_user_tweets_by_screen_name", "get_user_tweets_by_id", 
                          "get_friends_screen_names_by_screen_name", "get_friends_ids_by_id"]
        
        result = ""
        for function_name in functions_list:
            result += function_name + "\n"

        return result.strip()


if __name__ == "__main__":
    start_date = datetime.datetime(2019, 6, 1, 0, 0, 0)
    end_date =   datetime.datetime(2019, 10, 24, 0, 0, 0)
    
    # import tweepyDS
    # input_datastore = tweepyDS.TweepyDS()

    # import mongoDS
    # output_datastore = mongoDS.MongoDS()


    twitterDownloader = TwitterDownloader("init-algo.yaml")
    twitterDownloader.get_tweets("realDonaldTrump", start_date, end_date, 1)
    # twitterDownloader.get_friends_by_id(25073877, 5)
    twitterDownloader.get_friends_by_screen_name("realDonaldTrump", 5)
