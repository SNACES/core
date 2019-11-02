from typing import Union
from process import Process

import datetime

"""
Download Tweets for use in future algorithms.
"""
class TwitterTweetDownloader(Process):
    def __init__(self, init_path, input_DAOs={}, output_DAOs={}):
        Process.__init__(self, init_path, input_DAOs, output_DAOs)

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

        tweets = self.input_DAOs['TweepyClient'].read(query) 
        document = {
            "id": id,
            "start_date": start_date,
            "end_date": end_date,
            # "num_tweets": num_tweets
            "tweets": tweets
        }
        self.output_DAOs["getTweets"].create(document)

"""
Download Twitter Friends for use in future algorithms.
"""
class TwitterFriendsDownloader(Process):
    def __init__(self, init_path, input_DAOs={}, output_DAOs={}):
        Process.__init__(self, init_path, input_DAOs, output_DAOs)

    def get_friends_by_screen_name(self, screen_name: str, num_friends: int) -> list:
        """  
        Return a list of screen_names of friends of user with screen name screen_name.
        """
        
        assert type(screen_name) == str

        query = {"query_type": "get_friends_by_screen_name", 
                 "screen_name": screen_name,
                 "num_friends": num_friends}
        
        friends = self.input_DAOs['TweepyClient'].read(query)
        document = {
            "screen_name": screen_name,
            # "num_friends": num_friends,
            "friends": friends
        }
        self.output_DAOs["getFriendsByScreenName"].create(document)

    def get_friends_by_id(self, id: int, num_friends: int) -> list:
        """  
        Return a list of ids of friends of user with id id.
        """
        
        assert type(id) == int
        
        query = {"query_type": "get_friends_by_id", 
                 "id": id,
                 "num_friends": num_friends}

        friends = self.input_DAOs['TweepyClient'].read(query)
        document = {
            "id": id,
            # "num_friends": num_friends,
            "friends": friends
        }
        self.output_DAOs["getFriendsByID"].create(document)

def rate_limited_functions() -> str:
    functions_list = ["get_user_tweets_by_screen_name", "get_user_tweets_by_id", 
                      "get_friends_screen_names_by_screen_name", "get_friends_ids_by_id"]
    
    result = ""
    for function_name in functions_list:
        result += function_name + "\n"
    return result.strip()

if __name__ == "__main__":
    start_date = datetime.datetime(2019, 6, 1, 0, 0, 0)
    end_date =   datetime.datetime(2019, 11, 3, 0, 0, 0)
    
    twitterDownloader = TwitterTweetDownloader("init-algo.yaml")
    twitterDownloader.get_tweets("realDonaldTrump", start_date, end_date, 1)
    
    # twitterDownloader.get_friends_by_id(25073877, 5)
    # twitterDownloader.get_friends_by_screen_name("realDonaldTrump", 5)




    
