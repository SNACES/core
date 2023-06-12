from src.process.clustering.label_propagation_clusterer import LabelPropagationClusterer
from src.process.clustering.walktrap_clusterer_weighted import WalktrapClustererWeighted
from src.process.clustering.walktrap_clusterer_unweighted import WalktrapClustererUnweighted
from src.process.clustering.bayan_clusterer import BayanClusterer


from typing import Dict, List


class ClustererFactory():
    def create_clusterer(type, social_graph_getter, cluster_setter, user_friends_getter):
        # Uncomment desired clusterer algorithm

        # clusterer = LabelPropagationClusterer(social_graph_getter, cluster_setter, user_friends_getter)
        clusterer = WalktrapClustererWeighted(social_graph_getter, cluster_setter, user_friends_getter)
        # clusterer = WalktrapClustererUnweighted(social_graph_getter, cluster_setter, user_friends_getter)
        # clusterer = BayanClusterer(social_graph_getter, cluster_setter, user_friends_getter)

        return clusterer
