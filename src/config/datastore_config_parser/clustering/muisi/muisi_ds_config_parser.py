from src.config.datastore_config_parser.ds_config_parser import DSConfigParser
from src.dpi.dao_factory.mongo.clustering.muisi.muisi_mongo_dao_factory import MUISIMongoDAOFactory

class MUISIDSConfigParser(DSConfigParser):
    def __init__(self):
        self.mongo_dao_factory = MUISIMongoDAOFactory()

    def _get_muisi_setter(self, parsed_setter_config):
        return self._get_dao(parsed_setter_config, 'MUISI', True)
    
    def _get_muisi_getter(self, parsed_getter_config):
        return self._get_dao(parsed_getter_config, 'MUISI', False)