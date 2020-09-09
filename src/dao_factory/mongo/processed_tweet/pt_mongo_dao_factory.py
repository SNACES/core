from src.shared.mongo import get_collection_from_config
from src.datastore.mongo.processed_tweet.processed_tweet_mongo_set import ProcessedTweetMongoSetDAO
from src.datastore.mongo.processed_tweet.processed_tweet_mongo_get import ProcessedTweetMongoGetDAO

class ProcessedTweetMongoDAOFactory:
    def create_setter(self, processed_tweet_config):
        return self._create_processed_tweet_dao(processed_tweet_config, True)

    def create_getter(self, processed_tweet_config):
        return self._create_processed_tweet_dao(processed_tweet_config, False)

    def _create_processed_tweet_dao(self, processed_tweet_config, is_setter):
        processed_tweet_mongo_dao = ProcessedTweetMongoSetDAO() if is_setter else ProcessedTweetMongoGetDAO()

        global_tweets_config = processed_tweet_config['Global-Tweet'] if 'Global-Tweet' in processed_tweet_config else None
        user_tweets_config = processed_tweet_config['User-Tweet'] if 'User-Tweet' in processed_tweet_config else None

        # Get Global Tweets
        if global_tweets_config:
            processed_tweet_mongo_dao.global_processed_tweet_collection = get_collection_from_config(global_tweets_config)

        # Get User Tweets
        if user_tweets_config:
            processed_tweet_mongo_dao.user_processed_tweet_collection = get_collection_from_config(user_tweets_config)

        if not global_tweets_config and not user_tweets_config:
            processed_tweet_mongo_dao = None

        return processed_tweet_mongo_dao