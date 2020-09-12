from src.config.config_parser import ConfigParser
from src.config.datastore_config_parser.social_graph.social_graph_ds_config_parser import SocialGraphDSConfigParser
from src.config.datastore_config_parser.clustering.label_propagation.lp_ds_config_parser import LabelPropagationDSConfigParser

class LabelPropagationConfigParser(ConfigParser):
    def __init__(self, config_path):
        super().__init__(config_path)
        self.social_graph_ds_config_parser = SocialGraphDSConfigParser()
        self.lp_ds_config_parser = LabelPropagationDSConfigParser()

    def get_getters(self, parsed_getter_config):
        social_graph_getter = self.social_graph_ds_config_parser._get_social_graph_getter(parsed_getter_config)
        return social_graph_getter

    def get_setters(self, parsed_setter_config):
        lp_cluster_setter = self.lp_ds_config_parser._get_lp_setter(parsed_setter_config)
        return lp_cluster_setter