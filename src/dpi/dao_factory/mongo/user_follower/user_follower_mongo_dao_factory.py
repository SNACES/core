from src.shared.mongo import get_collection_from_config
from src.dpi.datastore.mongo.user_follower.user_followers_mongo_set import UserFollowersMongoSetDAO
from src.dpi.datastore.mongo.user_follower.user_followers_mongo_get import UserFollowersMongoGetDAO

class UserFollowerMongoDAOFactory:
    def create_setter(self, user_followers_config):
        return self._create_follower_dao(user_followers_config, True)
    
    def create_getter(self, user_followers_config):
        return self._create_follower_dao(user_followers_config, False)
        
    def _create_follower_dao(self, user_followers_config, is_setter):
        user_followers_dao = UserFollowersMongoSetDAO() if is_setter else UserFollowersMongoGetDAO()

        by_name_config = user_followers_config['User-Follower-By-Name'] if 'User-Follower-By-Name' in user_followers_config else None
        by_id_config = user_followers_config['User-Follower-By-ID'] if 'User-Follower-By-ID' in user_followers_config else None 

        if by_name_config:
            user_followers_dao.user_followers_by_name_collection = get_collection_from_config(by_name_config)
  
        if by_id_config:
            user_followers_dao.user_followers_by_id_collection = get_collection_from_config(by_id_config)

        if not by_name_config and not by_id_config:
            user_followers_dao = None

        return user_followers_dao