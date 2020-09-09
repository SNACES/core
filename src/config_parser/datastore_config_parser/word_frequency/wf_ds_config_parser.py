from src.config_parser.datastore_config_parser.ds_config_parser import DSConfigParser
from src.dao_factory.mongo.word_frequency.wf_mongo_dao_factory import WordFrequencyMongoDAOFactory

class WordFrequencyDSConfigParser(DSConfigParser):
    def __init__(self):
        self.mongo_dao_factory = WordFrequencyMongoDAOFactory()

    def _get_wf_setter(self, parsed_setter_config):
        return self._get_dao(parsed_setter_config, 'Word-Frequency', True)

    def _get_wf_getter(self, parsed_getter_config):
        return self._get_dao(parsed_getter_config, 'Word-Frequency', False)