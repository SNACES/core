import datetime

from src.process.twitter_download.twitter_downloader import TwitterTweetDownloader, TwitterFriendsDownloader, TwitterFollowersDownloader
from src.datastore.tweepy.tweepy_get import TweepyGetDAO
from src.datastore.mongo.raw_tweet.tweet_mongo_set import TweetMongoSetDAO
from src.datastore.mongo.user_friend.user_friends_mongo_set import UserFriendsMongoSetDAO
from src.datastore.mongo.user_follower.user_followers_mongo_set import UserFollowersMongoSetDAO

twitter_downloader = TwitterTweetDownloader()
friends_downloader = TwitterFriendsDownloader()
followers_downloader = TwitterFollowersDownloader()

# Init query variables
id = "animesh_garg"
start_date = datetime.datetime(2019, 6, 1, 0, 0, 0)
end_date = datetime.datetime(2020, 7, 17, 0, 0, 0)

# Init input and output daos
tweepy_get = TweepyGetDAO()

from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/') # "mongodb://localhost:2223"
tweet_mongo_set = TweetMongoSetDAO()
db = client['TwitterDownload-Test']

tweet_mongo_set.user_tweet_collection = db['UserTweets']
tweet_mongo_set.global_tweet_collection = db['GlobalTweets']

user_friends_set = UserFriendsMongoSetDAO()
user_friends_set.user_friends_by_name_collection = db['UserFriends']

user_followers_set = UserFollowersMongoSetDAO()
user_followers_set.user_followers_by_name_collection = db['UserFollowers']

# Test methods
# twitter_downloader.gen_user_tweets(id, tweepy_get, tweet_mongo_set, 20)
# twitter_downloader.gen_user_tweets(id, tweepy_get, tweet_mongo_set, 50, start_date, end_date)
# twitter_downloader.gen_random_tweet(tweepy_get, tweet_mongo_set)
# friends_downloader.gen_friends_by_screen_name(id, tweepy_get, user_friends_set, 10)
# followers_downloader.gen_followers_by_screen_name(id, tweepy_get, user_followers_set, 10)

