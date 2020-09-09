from src.config_parser.config_parser import ConfigParser
from src.dao_factory.mongo.user_friend.user_friend_mongo_dao_factory import UserFriendMongoDAOFactory

class UserFriendDSConfigParser(ConfigParser):
    def __init__(self, config_path):
        super().__init__(config_path)
        self.mongo_dao_factory = UserFriendMongoDAOFactory()

    def _get_user_friends_setter(self, parsed_setter_config):
        return self._get_dao(parsed_setter_config, 'User-Friend', True)
    
    def _get_user_friends_getter(self, parsed_getter_config):
        return self._get_dao(parsed_getter_config, 'User-Friend', False)

    # def _get_uf_dao(self, parsed_dao_config, is_setter):
    #     user_friends_config = parsed_dao_config['User-Friend'] if 'User-Friend' in parsed_dao_config else None
    #     if user_friends_config:
    #         if user_friends_config['type'] == "Mongo":
    #             mongo_dao_factory = UserFriendMongoDAOFactory()
    #             if is_setter:
    #                 user_friends_dao = mongo_dao_factory.create_user_friends_setter(user_friends_config)
    #             else:
    #                 user_friends_dao = mongo_dao_factory.create_user_friends_getter(user_friends_config)
    #         else:
    #             raise Exception("Datastore type not supported")

    #     return user_friends_dao

    