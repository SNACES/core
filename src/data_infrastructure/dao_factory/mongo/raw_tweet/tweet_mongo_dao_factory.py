from src.shared.mongo import get_collection_from_config
from src.data_infrastructure.datastore.mongo.raw_tweet.tweet_mongo_set import TweetMongoSetDAO
from src.data_infrastructure.datastore.mongo.raw_tweet.tweet_mongo_get import TweetMongoGetDAO

class TweetMongoDAOFactory():
    """
    A class that generates TweetDAO getter and setter.
    """
    def create_setter(self, tweet_config):
        """
        Create a Tweet MongoSetDAO with the config file.

        @param tweet_config: path of the config file
        @return: a required TweetMongoSetDAO
        """
        return self._create_tweet_dao(tweet_config, True)

    def create_getter(self, tweet_config):
        """
        Create a Tweet MongoGetDAO with the config file.

        @param tweet_config: the path of config file
        @return: a required Tweet MongoGetDAO
        """
        return self._create_tweet_dao(tweet_config, False)

    def _create_tweet_dao(self, tweet_config, is_setter):
        """
        Create a Tweet getter or setter as required. 
        For a getter dao, get the required data collection from MongoDB.
        For a setter dao, set the data collection into MongoDB.

        @param tweet_config: the config file path
        @param is_setter: True if TweetDao setter is required
        @return: a Tweet MongoDAO getter or a Tweet MongoDAO setter
        """
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
