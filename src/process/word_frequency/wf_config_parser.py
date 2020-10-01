from src.config.config_parser import ConfigParser
from src.config.datastore_config_parser.processed_tweet.pt_ds_config_parser import ProcessedTweetDSConfigParser
from src.config.datastore_config_parser.word_frequency.wf_ds_config_parser import WordFrequencyDSConfigParser

class WordFrequencyConfigParser(ConfigParser):
    """
    A subclass of ConfigParser that generate get and set DAO of Word Frequency.
    """
    def __init__(self, config_path):
        """
        initialize a new WordFrequencyConfigParser class.
        
        @param config_path: the path of config file.
        """
        super().__init__(config_path)
        self.pt_ds_config_parser = ProcessedTweetDSConfigParser()
        self.wf_ds_config_parser = WordFrequencyDSConfigParser()

    def get_getters(self, parsed_getter_config):
        """
        Generate a WordFrequency GetDAO and a ProcessedTweet GetDAO with the config file.

        @param parsed_getter_config: the path of config file.
        @return: a word frequency GetDAO
        """
        processed_tweet_getter = self.pt_ds_config_parser._get_processed_tweet_getter(parsed_getter_config)
        wf_getter = self.wf_ds_config_parser._get_wf_getter(parsed_getter_config)

        return processed_tweet_getter, wf_getter

    def get_setters(self, parsed_setter_config):
        """
        Generate the WordFrequency SetDAO with the config file.

        @param parsed_setter_config: the path of config file.
        @return: a word frequency SetDAO.
        """
        processed_tweet_setter = self.pt_ds_config_parser._get_processed_tweet_setter(parsed_setter_config)
        wf_setter = self.wf_ds_config_parser._get_wf_setter(parsed_setter_config)

        return processed_tweet_setter, wf_setter