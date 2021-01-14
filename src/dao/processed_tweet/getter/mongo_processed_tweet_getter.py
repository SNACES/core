from src.dao.processed_tweet.getter.processed_tweet_getter import ProcessedTweetGetter
from src.dao.mongo.mongo_dao import MongoDAO
from src.model.processed_tweet import ProcessedTweet
import bson


class MongoProcessedTweetGetter(ProcessedTweetGetter, MongoDAO):
    def get_user_processed_tweets(id: str):
        tweet_doc_list = self.collection.find({"user_id": bson.int64.Int64(user_id)})

        tweets = []
        for doc in tweet_doc_list:
            tweets.append(ProcessedTweet.fromDict(doc))

        return tweets
