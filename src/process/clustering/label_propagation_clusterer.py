from src.process.clustering.clusterer import Clusterer
from networkx.algorithms.community.label_propagation import label_propagation_communities
from src.model.cluster import Cluster

class LabelPropagationClusterer(Clusterer):
    def cluster(self, seed_id, params):
        social_graph = self.social_graph_getter.get_social_graph(seed_id, params)
        clusters_data = label_propagation_communities(social_graph.graph)

        clusters = []
        for data in clusters_data:
            users = list(data)
            if seed_id in users:
                users.remove(seed_id)

            cluster = Cluster(seed_id, users)
            clusters.append(cluster)

        self.cluster_setter.store_clusters(seed_id, clusters, params)
