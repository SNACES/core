from src.process.clustering.label_propagation_clusterer import LabelPropagationClusterer
from typing import Dict, List


class ClustererFactory():
    def create_clusterer(type, social_graph_getter, cluster_setter):
        clusterer = LabelPropagationClusterer(social_graph_getter, cluster_setter)

        return clusterer
