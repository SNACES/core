from src.config_parser.datastore_config_parser.ds_config_parser import DSConfigParser
from src.dao_factory.mongo.clustering.affinity_propagation.ap_mongo_dao_factory import AffinityPropagationMongoDAOFactory

class AffinityPropagationDSConfigParser(DSConfigParser):
    def __init__(self):
        self.mongo_dao_factory = AffinityPropagationMongoDAOFactory()

    def _get_ap_setter(self, parsed_setter_config):
        return self._get_dao(parsed_setter_config, 'Affinity-Propagation', True)

    def _get_ap_getter(self, parsed_getter_config):
        return self._get_dao(parsed_getter_config, 'Affinity-Propagation', False)
