from src.shared.mongo import get_collection_from_config
from src.data_infrastructure.datastore.mongo.raw_tweet.tweet_mongo_set import TweetMongoSetDAO
from src.data_infrastructure.datastore.mongo.raw_tweet.tweet_mongo_get import TweetMongoGetDAO

class TweetMongoDAOFactory():
    def create_setter(self, tweet_config):
        return self._create_tweet_dao(tweet_config, True)

    def create_getter(self, tweet_config):
        return self._create_tweet_dao(tweet_config, False)

    def _create_tweet_dao(self, tweet_config, is_setter):
        tweet_mongo_dao = TweetMongoSetDAO() if is_setter else TweetMongoGetDAO()

        global_tweets_config = tweet_config['Global-Tweet'] if 'Global-Tweet' in tweet_config else None
        user_tweets_config = tweet_config['User-Tweet'] if 'User-Tweet' in tweet_config else None

        # Get Global Tweets
        if global_tweets_config:
            tweet_mongo_dao.global_tweet_collection = get_collection_from_config(global_tweets_config)

        # Get User Tweets
        if user_tweets_config:
            tweet_mongo_dao.user_tweet_collection = get_collection_from_config(user_tweets_config)

        if not global_tweets_config and not user_tweets_config:
            tweet_mongo_dao = None

        return tweet_mongo_dao
