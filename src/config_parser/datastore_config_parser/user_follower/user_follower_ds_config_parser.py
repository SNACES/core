from src.config_parser.datastore_config_parser.ds_config_parser import DSConfigParser
from src.dao_factory.mongo.user_follower.user_follower_mongo_dao_factory import UserFollowerMongoDAOFactory

class UserFollowerDSConfigParser(DSConfigParser):
    def __init__(self):
        self.mongo_dao_factory = UserFollowerMongoDAOFactory()

    def _get_user_followers_setter(self, parsed_setter_config):
        return self._get_dao(parsed_setter_config, 'User-Follower', True)

    def _get_user_followers_getter(self, parsed_getter_config):
        return self._get_dao(parsed_getter_config, 'User-Follower', False)

    # def _get_follower_dao(self, parsed_dao_config, is_setter):
    #     user_followers_config = parsed_dao_config['User-Follower'] if 'User-Follower' in parsed_dao_config else None
    #     if user_followers_config:
    #         if user_followers_config['type'] == "Mongo":
    #             mongo_dao_factory = UserFollowerMongoDAOFactory()
    #             if is_setter:
    #                 user_followers_dao = mongo_dao_factory.create_user_followers_setter(user_followers_config)
    #             else:
    #                 user_followers_dao = mongo_dao_factory.create_user_followers_getter(user_followers_config)
    #         else:
    #             raise Exception("Datastore type not supported")

    #     return user_followers_dao