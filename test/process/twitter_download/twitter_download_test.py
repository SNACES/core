from src.process.twitter_download.twitter_downloader import *
from src.process.twitter_download.tweepy_input import *
from src.process.twitter_download.download_mongo_output import *
# from src.twitter_downloader.download_dao_factory import DownloadDAOFactory

# import os
# # note that we need to pass in full path
# ds_config_path = os.getcwd() + "/../General/ds-init-config.yaml"
# ds_config_path = ""

twitter_downloader = TwitterTweetDownloader()
friends_downloader = TwitterFriendsDownloader()
following_downloader = TwitterFollowingDownloader()

# Init query variables
id = "animesh_garg"
start_date = datetime.datetime(2019, 6, 1, 0, 0, 0)
end_date = datetime.datetime(2020, 7, 17, 0, 0, 0)

# Init input and output daos
tweepy_input = TweepyDAO()

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/') # "mongodb://localhost:2223"
download_mongo_output = DownloadMongoOutputDAO()
db = client['TwitterDownload']
download_mongo_output.user_tweet_collection = db['UserTweets']
download_mongo_output.user_timeframe_tweet_collection = db['UserTimeframeTweets']
download_mongo_output.user_friends_by_name_collection = db['UserFriendsName']
download_mongo_output.user_following_by_name_collection = db['UserFollowingName']

# Test methods
twitter_downloader.get_tweets_by_user(id, tweepy_input, download_mongo_output, 50)
# twitter_downloader.get_tweets_by_timeframe_user(id, start_date, end_date, tweepy_input, download_mongo_output, 1)
# friends_downloader.get_friends_by_screen_name(id, tweepy_input, download_mongo_output)
# following_downloader.get_following_by_screen_name(id, tweepy_input, download_mongo_output, 1)

