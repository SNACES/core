from src.process.raw_tweet_processing.raw_tweet_processor import *
from src.process.raw_tweet_processing.tweet_mongo_input import *
from src.process.raw_tweet_processing.tweet_mongo_output import *

tweet_processor = RawTweetProcessor()

# Init input and output daos
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
download_db = client['TwitterDownload']
processed_db = client['ProcessedTweets']

tweet_input = TweetMongoInputDAO()
tweet_input.user_tweets_collection = download_db['UserTweets'] 
tweet_input.global_tweets_collection = download_db['GlobalTweets'] 

tweet_output = TweetMongoOutputDAO()
tweet_output.user_tweets_collection = download_db['UserTweets'] 
tweet_output.user_processed_tweets_collection = processed_db['UserTweets']
tweet_output.global_processed_tweets_collection = processed_db['GlobalTweets']
tweet_output.global_tweets_collection = download_db['GlobalTweets'] 

# Run tests
# tweet_processor.gen_processed_user_tweets(tweet_input, tweet_output)
tweet_processor.gen_processed_global_tweets(tweet_input, tweet_output)
