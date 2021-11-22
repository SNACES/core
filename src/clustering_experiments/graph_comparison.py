from collections import Counter
import matplotlib.pyplot as plt
from src.shared.utils import get_project_root


def compare_number_clusters_user(initial_user: str):
    with open(f"{str(get_project_root())}/src/clustering_experiments/data/{initial_user}_number_of_clusters.txt", "r") as f:
        number_of_clusters_list = [int(num) for num in f.readlines()]
    with open(f"{str(get_project_root())}/src/clustering_experiments/data/{initial_user}_number_of_refined_clusters.txt", "r") as f:
        number_of_refined_clusters_list = [int(num) for num in f.readlines()]
    compare_number_clusters(number_of_clusters_list)
    compare_number_clusters(number_of_refined_clusters_list)

def compare_number_clusters(number_of_clusters_list: list):
    """Plots the number of clusters across experiment runs."""
    number_of_clusters_count = Counter(number_of_clusters_list).most_common()
    number_of_clusters, count = [num[0] for num in number_of_clusters_count], [num[1] for num in number_of_clusters_count]
    plt.bar(number_of_clusters, count)
    plt.show()

if __name__ == "__main__":
    compare_number_clusters_user("david_madras")
