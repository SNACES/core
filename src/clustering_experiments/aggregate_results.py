from compare_clustering_algorithms import get_clusters, threshold_clusters
from src.shared.utils import get_project_root

def write_cluster_sizes(initial_user: str, clusters, refined_clusters):
    """Write number of clusters to text files given clusters and refined_clusters of a particular experiment run."""
    with open(f"{str(get_project_root())}/src/clustering_experiments/data/{initial_user}_number_of_clusters.txt", "a") as f:
        f.write(str(len(clusters)) + "\n")
    with open(f"{str(get_project_root())}/src/clustering_experiments/data/{initial_user}_number_of_refined_clusters.txt", "a") as f:
        non_discarded_refined_clusters = threshold_clusters(refined_clusters)
        f.write(str(len(non_discarded_refined_clusters)) + "\n")

if __name__ == "__main__":
    clusters, refined_clusters = get_clusters("david_madras")
    write_cluster_sizes("david_madras", clusters, refined_clusters)
