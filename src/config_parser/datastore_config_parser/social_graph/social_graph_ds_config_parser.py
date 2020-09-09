from src.config_parser.datastore_config_parser.ds_config_parser import DSConfigParser
from src.dao_factory.mongo.social_graph.social_graph_mongo_dao_factory import SocialGraphMongoDAOFactory

class SocialGraphDSConfigParser(DSConfigParser):
    def __init__(self):
        self.mongo_dao_factory = SocialGraphMongoDAOFactory()

    def _get_social_graph_setter(self, parsed_setter_config):
        return self._get_dao(parsed_setter_config, 'Social-Graph', True)

    def _get_social_graph_getter(self, parsed_getter_config):
        return self._get_dao(parsed_getter_config, 'Social-Graph', False)
