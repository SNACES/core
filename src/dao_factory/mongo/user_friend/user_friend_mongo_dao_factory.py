from src.shared.mongo import get_collection_from_config
from src.datastore.mongo.user_friend.user_friends_mongo_set import UserFriendsMongoSetDAO
from src.datastore.mongo.user_friend.user_friends_mongo_get import UserFriendsMongoGetDAO

class UserFriendMongoDAOFactory():
    def create_setter(self, user_friends_config):
        return self._create_uf_dao(user_friends_config, True)
    
    def create_getter(self, user_friends_config):
        return self._create_uf_dao(user_friends_config, False)

    def _create_uf_dao(self, user_friends_config, is_setter):
        user_friends_dao = UserFriendsMongoSetDAO() if is_setter else UserFriendsMongoGetDAO()

        by_name_config = user_friends_config['User-Friend-By-Name'] if 'User-Friend-By-Name' in user_friends_config else None
        by_id_config = user_friends_config['User-Friend-By-ID'] if 'User-Friend-By-ID' in user_friends_config else None 

        if by_name_config:
            user_friends_dao.user_friends_by_name_collection = get_collection_from_config(by_name_config)
  
        if by_id_config:
            user_friends_dao.user_friends_by_id_collection = get_collection_from_config(by_id_config)

        if not by_name_config and not by_id_config:
            user_friends_dao = None

        return user_friends_dao