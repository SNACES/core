from src.config.datastore_config_parser.ds_config_parser import DSConfigParser
from src.data_infrastructure.dao_factory.mongo.raw_tweet.tweet_mongo_dao_factory import TweetMongoDAOFactory

class TweetDSConfigParser(DSConfigParser):
    def __init__(self):
        self.mongo_dao_factory = TweetMongoDAOFactory()

    def _get_tweet_setter(self, parsed_setter_config):
        return self._get_dao(parsed_setter_config, 'Tweet', True)

    def _get_tweet_getter(self, parsed_getter_config):
        return self._get_dao(parsed_getter_config, 'Tweet', False)

    # def _get_tweet_dao(self, parsed_dao_config, is_setter):
    #     tweet_config = parsed_dao_config['Tweet'] if 'Tweet' in parsed_dao_config else None

    #     if tweet_config:
    #         if tweet_config['type'] == "Mongo":
    #             mongo_dao_factory = TweetMongoDAOFactory()
    #             if is_setter:
    #                 tweet_mongo_dao = mongo_dao_factory.create_tweet_setter(tweet_config)  
    #             else:  
    #                 tweet_mongo_dao = mongo_dao_factory.create_tweet_getter(tweet_config)  
    #         else:
    #             raise Exception("Datastore type not supported")

    #     return tweet_mongo_dao