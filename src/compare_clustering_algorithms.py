from collections import defaultdict
import src.scripts.create_social_graph_and_cluster as csgc
import numpy as np
from typing import List, Dict
from src.model.cluster import Cluster
from pymongo import MongoClient

ITER_NUM = 5

def get_clusters(initial_user: str) -> tuple:
    """Returns the clusters using the old clustering algorithm and using the new clustering algorithm."""
    social_graph, local_neighbourhood = csgc.create_social_graph(initial_user)
    refined_social_graph = csgc.refine_social_graph(initial_user, social_graph, local_neighbourhood)
    clusters = csgc.clustering_from_social_graph(initial_user, social_graph)
    refined_clusters = csgc.clustering_from_social_graph(initial_user, refined_social_graph)

    return clusters, refined_clusters


def threshold_clusters(cluster:List[Cluster],  discard_threshold: int=10):
    "Discard cluster with size < discard_threshold and sort"
    refined_c = [c for c in cluster if len(c.users) > discard_threshold]
    refined_c.sort(key=lambda c: len(c.users), reverse=True)
    return refined_c


def compare_clusters(clusters_1:List[Cluster], clusters_2:List[Cluster], discard_threshold: int=10):
    "Compares clusters."
    refined_c1 = threshold_clusters(clusters_1)
    refined_c2 = threshold_clusters(clusters_2)

    subset_similarity_c1 = defaultdict(list)
    subset_similarity_c2 = defaultdict(list)

    for i1, c1 in enumerate(refined_c1):
        for i2, c2 in enumerate(refined_c2):
            subset_similarity_c1["Cluster " + str(i1) + " with length " + str(len(c1.users))].append((i2, check_clusters_subset(c2, c1), len(c2.users)))
            subset_similarity_c2["Cluster " + str(i2) + " with length " + str(len(c2.users))].append((i1, check_clusters_subset(c1, c2), len(c1.users)))

    # Sort in descending order of highest subset similarity
    for cluster in subset_similarity_c1:
        subset_similarity_c1[cluster].sort(key=lambda x: x[1], reverse=True)
    for cluster in subset_similarity_c2:
        subset_similarity_c2[cluster].sort(key=lambda x: x[1], reverse=True)

    return subset_similarity_c1, subset_similarity_c2


def check_clusters_subset(cluster_1, cluster_2) -> float:
    """Returns a value in [0, 1] indicating how much of cluster_1 is contained in the cluster_2."""
    c1_users = set(cluster_1.users)
    c2_users = set(cluster_2.users)
    return len(c1_users.intersection(c2_users)) / len(c2_users)


def count_clusters(cluster_list, discard_threshold:int):
    """Count how many clusters there are"""
    cluster_count = []
    for cluster_result in cluster_list:
        cluster_count.append(len(cluster_result.users))


if __name__ == "__main__":
    c1, c2 = get_clusters("david_madras")
    subset_similarity_c1, subset_similarity_c2 = compare_clusters(c1, c2)
    for k, v in subset_similarity_c1.items():
        print(k, v)
    # for k, v in subset_similarity_c2.items():
    #     print(k, v)
