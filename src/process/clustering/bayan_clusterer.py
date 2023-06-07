from src.process.clustering.clusterer import Clusterer
from src.model.cluster import Cluster
from src.shared.logger_factory import LoggerFactory

from collections import Counter

import networkx as nx
from networkx.utils import groups, not_implemented_for, py_random_state
import bayanpy

log = LoggerFactory.logger(__name__)

class BayanClusterer(Clusterer):
    def cluster_by_social_graph(self, seed_id, social_graph, params):
        clusters_data = []
        if social_graph.graph.number_of_nodes() > 0:
            clusters_data = bayanpy.bayan(social_graph.graph.to_undirected())[2]

        clusters = []
        for data in clusters_data:
            users = list(data)

            if str(seed_id) in users: # Why is this needed?
                users.remove(str(seed_id))

            #cleaned_users = self.clean_cluster_users(users)

            #cluster = Cluster(seed_id, cleaned_users)
            cluster = Cluster(seed_id, users)
            clusters.append(cluster)
            log.info(len(users))

        log.info("Number of clusters " + str(len(clusters)))

        self.cluster_setter.store_clusters(seed_id, clusters, params)
        return clusters
