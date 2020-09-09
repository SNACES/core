from src.config_parser.config_parser import ConfigParser
from src.config_parser.datastore_config_parser.raw_tweet.tweet_ds_config_parser import TweetDSConfigParser
from src.config_parser.datastore_config_parser.processed_tweet.pt_ds_config_parser import ProcessedTweetDSConfigParser

class RawTweetProcessingConfigParser(ConfigParser):
    def __init__(self, config_path):
        super().__init__(config_path)
        self.tweet_ds_config_parser = TweetDSConfigParser() 
        self.pt_ds_config_parser = ProcessedTweetDSConfigParser()

    def get_getters(self, parsed_getter_config):
        tweet_getter = self.tweet_ds_config_parser._get_tweet_getter(parsed_getter_config)
        return tweet_getter

    def get_setters(self, parsed_setter_config):
        tweet_setter = self.tweet_ds_config_parser._get_tweet_setter(parsed_setter_config)
        processed_tweet_setter = self.pt_ds_config_parser._get_processed_tweet_setter(parsed_setter_config)
        
        return tweet_setter, processed_tweet_setter