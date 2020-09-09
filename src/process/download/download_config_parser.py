from src.datastore.tweepy.tweepy_get import TweepyGetDAO
from src.config_parser.config_parser import ConfigParser
from src.config_parser.datastore_config_parser.raw_tweet.tweet_ds_config_parser import TweetDSConfigParser
from src.config_parser.datastore_config_parser.user_friend.user_friend_ds_config_parser import UserFriendDSConfigParser
from src.config_parser.datastore_config_parser.user_follower.user_follower_ds_config_parser import UserFollowerDSConfigParser

class DownloadConfigParser(ConfigParser):
    def __init__(self, config_path):
        super().__init__(config_path)
        self.tweet_ds_config_parser = TweetDSConfigParser() 
        self.user_friend_ds_config_parser = UserFriendDSConfigParser()
        self.user_follower_ds_config_parser = UserFollowerDSConfigParser()

    def get_getters(self, parsed_getter_config):
        tweepy_getter = self._get_tweepy_getter(parsed_getter_config)
        # This is for use in the Friends Downloader gen_user_local_neighborhood method 
        user_friends_getter = self.user_friend_ds_config_parser._get_user_friends_getter(parsed_getter_config)
        
        return tweepy_getter, user_friends_getter

    def get_setters(self, parsed_setter_config):
        tweet_setter = self.tweet_ds_config_parser._get_tweet_setter(parsed_setter_config)
        user_friends_setter = self.user_friend_ds_config_parser._get_user_friends_setter(parsed_setter_config)
        user_followers_setter = self.user_follower_ds_config_parser._get_user_followers_setter(parsed_setter_config)
        
        return tweet_setter, user_friends_setter, user_followers_setter

    def _get_tweepy_getter(self, parsed_getter_config):
        download_config = parsed_getter_config['Download-Source']
        if download_config:
            if download_config['type'] == "Tweepy": 
                return TweepyGetDAO()
            else:
                raise Exception("Datastore type not supported")
        else:
            raise Exception("Input config not set")


