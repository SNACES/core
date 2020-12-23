from typing import List, Dict
import bson
from src.model.tweet import Tweet
from src.model.user import User
from src.dao.raw_tweet.getter.raw_tweet_getter import RawTweetGetter


class MongoRawTweetGetter(RawTweetGetter):
    """
    Implementation of TweetGetter that retrieves tweets from MongoDB
    """

    def __init__(self):
        self.collection = None

    def set_tweet_collection(self, collection: str) -> None:
        self.collection = collection

    def get_tweet_by_id(self, id: str) -> Tweet:
        """
        Return tweet with id that matches the given id

        @param id the id of the tweet to get

        @return the Tweet object corresponding to the tweet id, or none if no
            tweet matches the given id
        """
        tweet_doc = self.collection.find_one({"id": bson.int64.Int64(id)})
        if tweet_doc is not None:
            return Tweet.fromDict(tweet_doc)
        else:
            return None

    def get_tweets_by_user(self, user: User) -> List[Tweet]:
        """
        Return a list of tweet with user_id that matches the given user

        @param user the user to retrieve tweets from
        """
        return self.get_tweets_by_user_id(user.id)

    def get_tweets_by_user_id(self, user_id: str) -> List[Tweet]:
        """
        Return a list of tweet with user_id that matches the given user_id

        @param user_id the id of the user to retrieve tweets from

        @return a list of tweets by the given user
        """

        tweet_doc_list = list(self.collection.find({"user_id": bson.int64.Int64(user_id)}))

        if len(tweet_doc_list) > 0:
            tweets = map(Tweet.fromDict, tweet_doc_list)
            return list(tweets)
        else:
            return None

    def contains_tweets_from_user(self, user_id: str):
        return self.collection.find_one({"user_id": bson.int64.Int64(user_id)}) is not None

    def get_num_tweets(self) -> int:
        """
        Returns the number of tweets in the mongo collection

        @return the number of tweets
        """
        # We call count with a blank query {} so that it returns an accurate
        # result, rather than relying on the metadata which gives an approximate
        # result. However this is slower
        return self.collection.count({})

    def get_retweets_of_user_by_user_id(self, user_id: str) -> List[Tweet]:
        retweet_doc_list = self.collection.find({"retweet_user_id": bson.int64.Int64(user_id)})

        retweets = []
        for doc in retweet_doc_list:
            retweets.append(Tweet.fromDict(doc))

        return retweets
