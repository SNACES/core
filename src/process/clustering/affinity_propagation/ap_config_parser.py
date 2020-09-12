from src.config.config_parser import ConfigParser
from src.config.datastore_config_parser.word_frequency.wf_ds_config_parser import WordFrequencyDSConfigParser
from src.config.datastore_config_parser.clustering.affinity_propagation.ap_ds_config_parser import AffinityPropagationDSConfigParser

class AffinityPropagationConfigParser(ConfigParser):
    def __init__(self, config_path):
        super().__init__(config_path)
        self.wf_ds_config_parser = WordFrequencyDSConfigParser()
        self.ap_ds_config_parser = AffinityPropagationDSConfigParser()

    def get_getters(self, parsed_getter_config):
        wf_getter = self.wf_ds_config_parser._get_wf_getter(parsed_getter_config)
        return wf_getter

    def get_setters(self, parsed_setter_config):
        aff_prop_setter = self.ap_ds_config_parser._get_ap_setter(parsed_setter_config)
        return aff_prop_setter