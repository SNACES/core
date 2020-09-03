from src.process.raw_tweet_processing.raw_tweet_processor import RawTweetProcessor
from src.datastore.mongo.raw_tweet.tweet_mongo_get import TweetMongoGetDAO
from src.datastore.mongo.raw_tweet.tweet_mongo_set import TweetMongoSetDAO
from src.datastore.mongo.processed_tweet.processed_tweet_mongo_set import ProcessedTweetMongoSetDAO

tweet_processor = RawTweetProcessor()

# Init input and output daos
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
download_db = client['TwitterDownload-Test']
processed_db = client['ProcessedTweets-Test']

tweet_get = TweetMongoGetDAO()
tweet_get.user_tweets_collection = download_db['UserTweets'] 
tweet_get.global_tweets_collection = download_db['GlobalTweets'] 

tweet_set = TweetMongoSetDAO()
tweet_set.user_tweet_collection = download_db['UserTweets']
tweet_set.global_tweet_collection = download_db['GlobalTweets']

processed_tweet_set = ProcessedTweetMongoSetDAO()
processed_tweet_set.user_processed_tweets_collection = processed_db['UserTweets']
processed_tweet_set.global_processed_tweets_collection = processed_db['GlobalTweets']

# Run tests
# tweet_processor.gen_processed_global_tweets(tweet_get, tweet_set, processed_tweet_set)
# tweet_processor.gen_processed_user_tweets(tweet_get, tweet_set, processed_tweet_set)
