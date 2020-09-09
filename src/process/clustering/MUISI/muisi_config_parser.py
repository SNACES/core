from src.config_parser.config_parser import ConfigParser
from src.config_parser.datastore_config_parser.word_frequency.wf_ds_config_parser import WordFrequencyDSConfigParser
from src.config_parser.datastore_config_parser.raw_tweet.tweet_ds_config_parser import TweetDSConfigParser
from src.config_parser.datastore_config_parser.clustering.muisi.muisi_ds_config_parser import MUISIDSConfigParser

class MUISIConfigParser(ConfigParser):
    def __init__(self, config_path, is_retweets_mode):
        super().__init__(config_path)
        self.wf_ds_config_parser = WordFrequencyDSConfigParser()
        self.tweet_ds_config_parser = TweetDSConfigParser() 
        self.muisi_ds_config_parser = MUISIDSConfigParser()
        self.is_retweets_mode = is_retweets_mode

    def get_getters(self, parsed_getter_config):
        if self.is_retweets_mode:
            getter = self.tweet_ds_config_parser._get_tweet_getter(parsed_getter_config)
        else:
            getter = self.wf_ds_config_parser._get_wf_getter(parsed_getter_config)
        return getter

    def get_setters(self, parsed_setter_config):
        muisi_setter = self.muisi_ds_config_parser._get_muisi_setter(parsed_setter_config)
        return muisi_setter


