from src.config_parser.config_parser import ConfigParser
from src.config_parser.datastore_config_parser.user_friend.user_friend_ds_config_parser import UserFriendDSConfigParser
from src.config_parser.datastore_config_parser.social_graph.social_graph_ds_config_parser import SocialGraphDSConfigParser

class SocialGraphConfigParser(ConfigParser):
    def __init__(self, config_path):
        super().__init__(config_path)
        self.user_friend_ds_config_parser = UserFriendDSConfigParser()
        self.social_graph_ds_config_parser = SocialGraphDSConfigParser()

    def get_getters(self, parsed_getter_config):
        user_friends_getter = self.user_friend_ds_config_parser._get_user_friends_getter(parsed_getter_config)
        return user_friends_getter

    def get_setters(self, parsed_setter_config):
        social_graph_setter = self.social_graph_ds_config_parser._get_social_graph_setter(parsed_setter_config)
        return social_graph_setter