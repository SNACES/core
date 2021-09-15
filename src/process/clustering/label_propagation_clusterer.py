from src.process.clustering.clusterer import Clusterer
from src.model.cluster import Cluster
from src.shared.logger_factory import LoggerFactory

from collections import Counter

import networkx as nx
from networkx.utils import groups, not_implemented_for, py_random_state

log = LoggerFactory.logger(__name__)

class LabelPropagationClusterer(Clusterer):
    def cluster(self, seed_id, params):
        social_graph = self.social_graph_getter.get_social_graph(seed_id, params)
        self.cluster_by_social_graph(seed_id, social_graph, params)

    def cluster_by_social_graph(self, seed_id, social_graph, params):
        clusters_data = [item for item in label_propagation_communities(social_graph.graph)]

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

    def cluster_by_graph(self, seed_id, graph):
        clusters_data = [item for item in label_propagation_communities(graph)]

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

        return clusters

    def clean_cluster_users(self, users):
        """
        Removes all user in users who don't follow anyone else in the list
        """
        clean = False
        while not clean:
            new_friends = []
            for user in users:
                friends = self.user_friend_getter.get_user_friends_ids(user)
                if len([friend for friend in users if (friend in friends)]) > 0:
                    new_friends.append(user)
            if set(new_friends) == set(users):
                clean = True
            else:
                users = new_friends
        return users


def label_propagation_communities(G):
    coloring = color_network(G)
    # Create a unique label for each node in the graph
    labeling = {v: k for k, v in enumerate(G)}
    while not labeling_complete(labeling, G):
        for color, nodes in coloring.items():
            for n in nodes:
                update_label(n, labeling, G)
    # log.info(set(labeling.values()))
    for label in set(labeling.values()):
        yield {x for x in labeling if labeling[x] == label}

def color_network(G):
    """
    Colors a network so that neighbouring nodes all have distinct colors.

    Returns a dictionary where the keys are colors, and the values are sets
    of nodes
    """
    coloring = dict()
    colors = nx.coloring.greedy_color(G)
    for node, color in colors.items():
        if color in coloring:
            coloring[color].add(node)
        else:
            coloring[color] = {node}
    return coloring

def labeling_complete(labeling, G):
    """
    Returns true if label propogation algorithm has completed
    """
    return all(
        labeling[v] in most_frequent_labels(v, labeling, G) for v in G if len(G[v]) > 0
    )

def most_frequent_labels(node, labeling, G):
    """
    Returns a set of all labels with maximum frequency in 'labeling'.
    """
    if not G[node]:
        return {labeling[node]}

    freqs = Counter(labeling[q] for q in G[node])
    max_freq = max(freqs.values())
    return {label for label, freq in freqs.items() if freq == max_freq}

def update_label(node, labeling, G):
    high_labels = most_frequent_labels(node, labeling, G)
    if len(high_labels) == 1:
        labeling[node] = high_labels.pop()
    elif len(high_labels) > 1:
        # Prec-Max
        if labeling[node] not in high_labels:
            labeling[node] = max(high_labels)
