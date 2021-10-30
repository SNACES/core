from collections import defaultdict
import src.clustering_experiments.create_social_graph_and_cluster as csgc
import numpy as np
from typing import List, Dict
from src.model.cluster import Cluster
from pymongo import MongoClient
from src.clustering_experiments.compare_clustering_algorithms import *
from src.clustering_experiments.clustering_data import get_all_data, format_all_data


def categorize_clusters_by_length(all_clusters):
    """
    Given a list containing clustering results
    Refine/Sort the clusters, and split them into three list based on length
    """
    refined_cluster_list = []
    # single_clustering_entry is data from 1 run of the clustering algo
    # is dictionary with fields 'clusters' and 'num'
    # each 'clusters' is dictionary with 'base_user' and 'users'
    for clusters in all_clusters:
        refined_cluster_list.append(threshold_clusters(clusters))

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


# If we get are the clustering contents same across same size clusters?
def compare_same_size_clusters(all_clusters):
    """
    Given a list containing list of cluster of same size,
    Return average/variance of each size, along with the jaccard similarity over all
    TODO: Note this is incomplete as the clusters remained the same throughout one execution
    """
    # store the list of clusters_dictionary for each clustering run

    list1, list2, list3 = categorize_clusters_by_length(all_clusters)
    print(set(list2[0][0].users).intersection(set(list2[0][1].users)))
    experiment_results("david_madras", list2[0], list2[1])
    experiment_results("david_madras", list3[0], list3[1])
    experiment_results("david_madras", list2[0], list3[0])
    # TODO: aggregate data, the above code only computes between three sets of results


def experiment_results(initial_user: str, c1, c2):
    """Writes the clustering comparison experiment results for the screen_name."""
    with open(f"./src/clustering_experiments/{initial_user}_clustering_samesize_results.txt", "a") as f:
        subset_similarity_clusters, subset_similarity_refined_clusters = compare_clusters(c1, c2)
        f.write("-" * 20 + "\n")
        for refined_cluster in subset_similarity_refined_clusters:
            f.write(f"Cluster {refined_cluster[0]} of size {refined_cluster[1]}: \n")
            for cluster in subset_similarity_refined_clusters[refined_cluster]:
                f.write(f"\t is contained in Cluster {cluster[0]} of size {cluster[2]} about {round(cluster[1] * 100, 2)}%. \n")

if __name__ == "__main__":
    # generate cluster data and store in mongodb

    all_data = get_all_data()
    # each datapoint is result from one clustering
    # each datapoint has 'num' and 'clusters'

    all_clusters = format_all_data(all_data)
    # This formats each cluster in data['clusters'] from dict to Cluster object

    compare_same_size_clusters(all_clusters)
