from src.shared.config_parser import ConfigParser
from src.datastore.tweepy.tweepy_get import TweepyGetDAO
from src.process.download.dao_factory.download_mongo_dao_factory import DownloadMongoDAOFactory

class DownloadConfigParser(ConfigParser):
    def get_getters(self, parsed_getter_config):
        tweepy_getter = self._get_tweepy_getter(parsed_getter_config)
        return tweepy_getter

    def get_setters(self, parsed_setter_config):
        tweet_setter = self._get_tweet_setter(parsed_setter_config)
        user_friends_setter = self._get_user_friends_setter(parsed_setter_config)
        user_followers_setter = self._get_user_followers_setter(parsed_setter_config)
        
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

    def _get_tweet_setter(self, parsed_setter_config):
        tweet_config = parsed_setter_config['Tweet'] if 'Tweet' in parsed_setter_config else None

        if tweet_config:
            if tweet_config['type'] == "Mongo":
                mongo_dao_factory = DownloadMongoDAOFactory()
                tweet_mongo_setter = mongo_dao_factory.create_tweet_setter(tweet_config)    
            else:
                raise Exception("Datastore type not supported")

        return tweet_mongo_setter

    def _get_user_friends_setter(self, parsed_setter_config):
        user_friends_config = parsed_setter_config['User-Friend'] if 'User-Friend' in parsed_setter_config else None
        if user_friends_config:
            if user_friends_config['type'] == "Mongo":
                mongo_dao_factory = DownloadMongoDAOFactory()
                user_friends_setter = mongo_dao_factory.create_user_friends_setter(user_friends_config)
            else:
                raise Exception("Datastore type not supported")

        return user_friends_setter

    def _get_user_followers_setter(self, parsed_setter_config):
        user_followers_config = parsed_setter_config['User-Follower'] if 'User-Follower' in parsed_setter_config else None
        if user_followers_config:
            if user_followers_config['type'] == "Mongo":
                mongo_dao_factory = DownloadMongoDAOFactory()
                user_followers_setter = mongo_dao_factory.create_user_followers_setter(user_followers_config)
            else:
                raise Exception("Datastore type not supported")

        return user_followers_setter

