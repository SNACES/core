from collections import defaultdict
import src.clustering_experiments.create_social_graph_and_cluster as csgc
import numpy as np
from typing import List, Dict
from src.model.cluster import Cluster

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
            # Measure how much c1 is contained in c2
            subset_similarity_c1[(i1, len(c1.users))].append((i2, check_clusters_subset(c1, c2), len(c2.users)))
            # Measure how much c2 is contained in c1
            subset_similarity_c2[(i2, len(c2.users))].append((i1, check_clusters_subset(c2, c1), len(c1.users)))

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
    return len(c1_users.intersection(c2_users)) / len(c1_users)


def count_clusters(cluster_list, discard_threshold:int):
    """Count how many clusters there are"""
    cluster_count = []
    for cluster_result in cluster_list:
        cluster_count.append(len(cluster_result.users))

def experiment_results(initial_user: str):
    """Writes the clustering comparison experiment results for the screen_name."""
    with open(f"./src/clustering_experiments/data/{initial_user}_clustering_comparison_results.txt", "a") as f:
        clusters, refined_clusters = get_clusters(initial_user)
        subset_similarity_clusters, subset_similarity_refined_clusters = compare_clusters(clusters, refined_clusters)
        f.write("-" * 20 + "\n")
        for refined_cluster in subset_similarity_refined_clusters:
            f.write(f"Refined Cluster {refined_cluster[0]} of size {refined_cluster[1]}: \n")
            for cluster in subset_similarity_refined_clusters[refined_cluster]:
                f.write(f"\t is contained in Cluster {cluster[0]} of size {cluster[2]} about {round(cluster[1] * 100, 2)}%. \n")

if __name__ == "__main__":
    experiment_results("timnitGebru")
    pass
