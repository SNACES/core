from src.process.clustering.clusterer import Clusterer
from src.process.clustering.label_propagation_clusterer import LabelPropagationClusterer
from src.dao.cluster.cluster_dao_factory import ClusterDAOFactory
from src.dao.social_graph.social_graph_dao_factory import SocialGraphDAOFactory
from typing import Dict


class ClusterSocialGraphActivity():
    """
    """

    def __init__(self, config: Dict):
        self.clusterer = None

        self.configure(config)

    def configure(self, config: Dict):
        if config is not None:
            # Configure input datastore
            input_datastore = config["input-datastore"]
            social_graph = input_datastore["SocialGraph"]

            social_graph_getter = SocialGraphDAOFactory.create_getter(social_graph)

            # Configure output datastore
            output_datastore = config["output-datastore"]
            cluster = output_datastore["Cluster"]

            cluster_setter = ClusterDAOFactory.create_setter(cluster)

            self.clusterer = LabelPropagationClusterer(social_graph_getter, cluster_setter)

    def cluster_social_graph(self, seed_id, params):
        if params is None:
            params = {"graph_type": "union"}
        self.clusterer.cluster(seed_id, params)
