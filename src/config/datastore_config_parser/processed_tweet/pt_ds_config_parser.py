from src.config.datastore_config_parser.ds_config_parser import DSConfigParser
from src.data_infrastructure.dao_factory.mongo.processed_tweet.pt_mongo_dao_factory import ProcessedTweetMongoDAOFactory

class ProcessedTweetDSConfigParser(DSConfigParser):
    def __init__(self):
        self.mongo_dao_factory = ProcessedTweetMongoDAOFactory()

    def _get_processed_tweet_setter(self, parsed_setter_config):
        return self._get_dao(parsed_setter_config, 'Processed-Tweet', True)
    
    def _get_processed_tweet_getter(self, parsed_getter_config):
        return self._get_dao(parsed_getter_config, 'Processed-Tweet', False)

                




