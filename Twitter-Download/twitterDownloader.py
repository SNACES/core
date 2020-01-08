import sys
sys.path.append('../General')
sys.path.append('../Concrete-DAO')

import functools 
from typing import Union, List
from process import Process

import datetime

"""
Download Tweets for use in future algorithms.
"""
class TwitterTweetDownloader(Process):
    def __init__(self, init_path, input_DAOs={}, output_DAOs={}):
        Process.__init__(self, init_path, input_DAOs, output_DAOs)

    def get_tweets_by_timeframe_user(self, start_date: datetime,
                   end_date: datetime, num_tweets: int, id: Union[str, int]=None, user_list_file_path=None) -> list:
        """
        Return num_tweets tweets made by user with id(username or user id) id between start_date and end_date.
        """
        
        # def list_path_handler(self):
        #     user_list_processor = UserListProcessor()
        #     user_list = user_list_processor.user_list_parser(user_list_file_path)
        #     user_list_processor.download_function_by_user_list(self.get_tweets_by_timeframe_user, user_list, start_date, end_date, num_tweets)
        
        # def user_handler(self):

        # process_user_or_list_path(id, user_list_file_path, list_path_handler, user_handler)

        if id is None and user_list_file_path is not None:
            user_list_processor = UserListProcessor()
            user_list = user_list_processor.user_list_parser(user_list_file_path)
            user_list_processor.download_function_by_user_list(self.get_tweets_by_timeframe_user, user_list, start_date, end_date, num_tweets)

        elif id is not None and user_list_file_path is None:
            query = {
                "query_type": "get_tweets_by_timeframe_user",
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
            self.output_DAOs["getTweetsByTimeframeUser"].create(document)
        else: 
            raise Exception("Please pass in exclusively either an id or a user list file path.")

    def get_tweets_by_user(self, id: Union[str, int], num_tweets: int) -> list:
        query = {"query_type": "get_tweets_user",
                 "id": id, 
                 "num_tweets": num_tweets
                 }

        tweets = self.input_DAOs['TweepyClient'].read(query) 
        document = {
            "id": id,
            # "num_tweets": num_tweets
            "tweets": tweets
        }
        self.output_DAOs["getTweetsByUser"].create(document)

    def get_random_tweets(self, num_tweets: int, output_collection_name: str, ds_location="", mongo_database_name="") -> list:
        query = {
            "query_type": "get_random_tweets",
            "num_tweets": num_tweets
        }
        tweets = self.input_DAOs['TweepyClient'].read(query) 
        
        # TODO: hmm, how should this be stored?
        documents = [{"tweet": tweet} for tweet in tweets]
        
        for document in documents:
            if output_collection_name not in self.output_DAOs:
                # we assume for now we want a MongoDAO
                # ds_location and mongo_database are provided in the case that we want to dynamically create a new collection
                self.output_DAOs[output_collection_name] = MongoOutputDAO(ds_location, mongo_database_name, output_collection_name)
            self.output_DAOs[output_collection_name].create(document)

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


"""
Download Twitter Following for use in future algorithms.
"""
class TwitterFollowingDownloader(Process):
    def __init__(self, init_path, input_DAOs={}, output_DAOs={}):
        Process.__init__(self, init_path, input_DAOs, output_DAOs)

    def get_following_by_screen_name(self, screen_name: str, num_following: int) -> list:
        assert type(screen_name) == str

        query = {"query_type": "get_following_by_screen_name", 
                 "screen_name": screen_name,
                 "num_following": num_following}
        
        following_users_screen_name = self.input_DAOs['TweepyClient'].read(query)
        document = {
            "screen_name": screen_name,
            "following_users_screen_name": following_users_screen_name
        }
        self.output_DAOs["getFollowingByScreenName"].create(document)

    def get_following_by_id(self, id: int, num_following: int) -> list:
        assert type(id) == int
        
        query = {"query_type": "get_following_by_screen_name", 
                 "id": id,
                 "num_following": num_following}

        following_users_ID = self.input_DAOs['TweepyClient'].read(query)
        document = {
            "id": id,
            "following_users_ID": following_users_ID
        }
        self.output_DAOs["getFollowingByID"].create(document)


def rate_limited_functions() -> str:
    functions_list = ["get_user_tweets_by_screen_name", "get_user_tweets_by_id", 
                      "get_friends_screen_names_by_screen_name", "get_friends_ids_by_id"]
    
    result = ""
    for function_name in functions_list:
        result += function_name + "\n"
    return result.strip()

class UserListProcessor:
    """
    Return a list of users given the path to a file containing a list of users.
    """
    def user_list_parser(self, user_list_file_path):
        with open(user_list_file_path, 'r') as stream:
            return [user.strip() for user in stream]

    """
    Precondition: argsv matches the args for download_function
    """
    def download_function_by_user_list(self, download_function, user_list, *argv):
        curried_operation = lambda acc, id: download_function(*argv, id) # acc is a dummy var
        
        self.process_user_list(user_list, curried_operation)

    def process_user_list(self, user_list, curried_function):
        functools.reduce(curried_function, user_list) 

if __name__ == "__main__":
    start_date = datetime.datetime(2019, 6, 1, 0, 0, 0)
    end_date =   datetime.datetime(2019, 11, 26, 0, 0, 0)
    
    import os
    # note that we need to pass in full path
    ds_config_path = os.getcwd() + "/../General/ds-init-config.yaml"
    twitterDownloader = TwitterTweetDownloader(ds_config_path)
    # twitterDownloader.get_tweets_by_user(1, )
    # twitterDownloader.get_tweets_by_timeframe_user(start_date, end_date, 1, user_list_file_path="user_list")
    
    # twitterDownloader.get_random_tweets(1)

    # twitterDownloader = TwitterFriendsDownloader(os.getcwd() + "/../General/ds-init-config.yaml")
    # twitterDownloader.get_friends_by_id(25073877, 5)
    # twitterDownloader.get_friends_by_screen_name("realDonaldTrump", 5)

    # twitterDownloader.get_friends_by_screen_name(user_name, num_friends_to_get)

    # following_downloader = TwitterFollowingDownloader(ds_config_path)
    # following_downloader.get_following_by_screen_name("Twitter", 5)

# twitter_downloader.get_tweets_by_timeframe_user(id, start_date, end_date: datetime, num_tweets)