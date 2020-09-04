from src.process.clustering.MUISI.retweets.muisi_retweet import MUISIRetweet, MUISIRetweetConfig
from src.datastore.mongo.raw_tweet.tweet_mongo_get import TweetMongoGetDAO
from src.datastore.mongo.cluster.MUISI.retweets.muisi_retweets_mongo_set import MUISIRetweetsMongoSetDAO

# Init input and output daos
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
tweet_db = client['TwitterDownload-Test']
muisi_db = client['RetweetMUISI-Test']

tweet_getter = TweetMongoGetDAO()
tweet_getter.user_tweets_collection = tweet_db['UserTweets']

muisi_cluster_setter = MUISIRetweetsMongoSetDAO()
muisi_cluster_setter.muisi_retweets_cluster_collection = muisi_db['MUISIRetweetClusters']

# Run tests
intersection_min = 2
popularity = 0.3
user_count = 5
muisi_config = MUISIRetweetConfig(intersection_min, popularity, user_count)

muisi = MUISIRetweet()
muisi.gen_clusters(muisi_config, tweet_getter, muisi_cluster_setter)
