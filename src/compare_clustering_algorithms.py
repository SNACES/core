from collections import defaultdict
import src.scripts.create_social_graph_and_cluster as csgc
import numpy as np

ITER_NUM = 5

def get_clusters(initial_user: str) -> tuple:
    """Returns the clusters using the old clustering algorithm and using the new clustering algorithm."""
    social_graph, local_neighbourhood = csgc.create_social_graph(initial_user)
    refined_social_graph = csgc.refine_social_graph(initial_user, social_graph, local_neighbourhood)
    clusters = csgc.clustering_from_social_graph(initial_user, social_graph)
    refined_clusters = csgc.clustering_from_social_graph(initial_user, refined_social_graph)

    return clusters, refined_clusters

def threshold_clusters(cluster,  discard_threshold: int=10):
    "Discard cluster with size < discard_threshold and sort"
    refined_c = [c for c in cluster if len(c.users) > discard_threshold]
    refined_c.sort(key=lambda c: len(c.users), reverse=True)
    return refined_c

def compare_clusters(clusters_1, clusters_2, discard_threshold: int=10):
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
    """Count how many clustrs there are"""
    cluster_count = []
    for cluster_result in cluster_list:
        cluster_count.append(len(cluster_result.users))

def categorize_clusters_by_length(cluster_list):
    """
    Given a list containing clustering results
    Refine/Sort the clusters, and split them into three list based on length
    """
    refined_cluster_list = []
    for cluster_result in cluster_list:
        refined_cluster_list.append(threshold_clusters(cluster_result))

    single_cluster_list = []
    double_cluster_list = []
    triple_cluster_list = []

    for refined_clusters in refined_cluster_list:
        if len(refined_clusters) == 1:
            single_cluster_list.append(refined_clusters)
        elif len(refined_clusters) == 2:
            double_cluster_list.append(refined_clusters)
        elif len(refined_clusters) == 3:
            triple_cluster_list.append(refined_clusters)

    return single_cluster_list, double_cluster_list, triple_cluster_list


def compare_same_size_clusters(cluster_list):
    """
    Given a list containing list of cluster of same size,
    Return average/variance of each size, along with the jaccard similarity over all
    TODO: Note this is incomplete as the clusters remained the same throughout one execution
    """
    cluster_size_list = []

    for cluster_result in cluster_list:
        cluster_size = [len(cluster.users) for cluster in cluster_result]
        cluster_size_list.append(cluster_size)

    print(cluster_size_list)
    cluster_size_arr = np.array(cluster_size_list)
    #cluster_size_mean = np.mean(np.transpose(cluster_size_arr))
    #cluster_size_std = np.std(np.transpose(cluster_size_arr))




# def interpret_subset_similarity_results(subse)


if __name__ == "__main__":
    c1, c2 = get_clusters("david_madras")
    subset_similarity_c1, subset_similarity_c2 = compare_clusters(c1, c2)
    for k, v in subset_similarity_c1.items():
        print(k, v)
    # for k, v in subset_similarity_c2.items():
    #     print(k, v)

    unrefined_clusters = []
    refined_clusters = []
    for i in range(ITER_NUM):
        c3, c4 = get_clusters("david_madras")
        unrefined_clusters.append(c3)
        refined_clusters.append(c4)

    single_clusters, double_clusters, triple_clusters = \
        categorize_clusters_by_length(refined_clusters)

    if len(triple_clusters) != 0:
        compare_same_size_clusters(triple_clusters)
    elif len(double_clusters) != 0:
        compare_same_size_clusters(double_clusters)
