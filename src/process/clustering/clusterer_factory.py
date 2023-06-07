from src.process.clustering.label_propagation_clusterer import LabelPropagationClusterer
from src.process.clustering.walktrap_clusterer import WalktrapClusterer
from src.process.clustering.bayan_clusterer import BayanClusterer


from typing import Dict, List


class ClustererFactory():
    def create_clusterer(type, social_graph_getter, cluster_setter, user_friends_getter):
        # Uncomment desired clusterer algorithm

        # clusterer = LabelPropagationClusterer(social_graph_getter, cluster_setter, user_friends_getter)
        # clusterer = WalktrapClusterer(social_graph_getter, cluster_setter, user_friends_getter)
        clusterer = BayanClusterer(social_graph_getter, cluster_setter, user_friends_getter)

        return clusterer
