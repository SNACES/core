from src.config.datastore_config_parser.ds_config_parser import DSConfigParser
from src.dpi.dao_factory.mongo.clustering.label_propagation.lp_mongo_dao_factory import LabelPropagationMongoDAOFactory

class LabelPropagationDSConfigParser(DSConfigParser):
    def __init__(self):
        self.mongo_dao_factory = LabelPropagationMongoDAOFactory()

    def _get_lp_setter(self, parsed_setter_config):
        return self._get_dao(parsed_setter_config, 'Label-Propagation', True)

    def _get_lp_getter(self, parsed_getter_config):
        return self._get_dao(parsed_getter_config, 'Label-Propagation', False)

