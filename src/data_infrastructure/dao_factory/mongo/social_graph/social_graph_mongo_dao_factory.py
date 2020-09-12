from src.shared.mongo import get_collection_from_config
from src.data_infrastructure.datastore.mongo.social_graph.social_graph_mongo_set import SocialGraphMongoSetDAO
from src.data_infrastructure.datastore.mongo.social_graph.social_graph_mongo_get import SocialGraphMongoGetDAO

class SocialGraphMongoDAOFactory():
    def create_setter(self, social_graph_config):
        return self._create_social_graph_dao(social_graph_config, True)

    def create_getter(self, social_graph_config):
        return self._create_social_graph_dao(social_graph_config, False)

    def _create_social_graph_dao(self, social_graph_config, is_setter):
        social_graph_mongo_dao = SocialGraphMongoSetDAO() if is_setter else SocialGraphMongoGetDAO()
        user_friend_graph_config = social_graph_config['User-Friend-Graph']
        
        if user_friend_graph_config:
            social_graph_mongo_dao.user_friends_graph_collection = get_collection_from_config(user_friend_graph_config)
        else:
            social_graph_mongo_dao = None
        
        return social_graph_mongo_dao