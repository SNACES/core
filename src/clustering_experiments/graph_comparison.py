from collections import Counter
import matplotlib.pyplot as plt
from src.shared.utils import get_project_root
from src.clustering_experiments.clustering_data import *
from ranking_users_in_clusters import rank_users


def compare_number_clusters_user(initial_user: str):
    with open(f"{str(get_project_root())}/src/clustering_experiments/data/{initial_user}_number_of_clusters.txt", "r") as f:
        number_of_clusters_list = [int(num) for num in f.readlines()]
    with open(f"{str(get_project_root())}/src/clustering_experiments/data/{initial_user}_number_of_refined_clusters.txt", "r") as f:
        number_of_refined_clusters_list = [int(num) for num in f.readlines()]
    compare_number_clusters(number_of_clusters_list)
    compare_number_clusters(number_of_refined_clusters_list)

def compare_number_clusters(number_of_clusters_list: list, refined=False, colour="blue", save=False, filename="test"):
    """Plots the number of clusters across experiment runs."""
    number_of_clusters_count = Counter(number_of_clusters_list).most_common()
    number_of_clusters, count = [num[0] for num in number_of_clusters_count], [num[1] for num in number_of_clusters_count]

    if refined:
        title = f"Number of Refined Clusters over {len(number_of_clusters_list)} runs"
    else:
        title = f"Number of Clusters over {len(number_of_clusters_list)} runs"

    fig, ax = plt.subplots()
    ax.bar(number_of_clusters, count, color=colour)
    ax.set_xlabel("Number of Clusters")
    ax.set_ylabel("Count across runs")
    ax.set_xticks(range(0, max(number_of_clusters) + 1))
    ax.set_yticks(range(0, len(number_of_clusters_list) + 1, len(number_of_clusters_list) // 5))
    ax.set_title(title)

    if save:
        plt.savefig(f'./src/clustering_experiments/data/img/{filename}')
    else:
        plt.show()

def compare_top_users_user(initial_user: str, num_clusters: int=2, num_refined_clusters: int=3, runs: int=10, save=False):
    """Compares the top 10 users for each cluster across runs with have num_clusters each run."""
    def helper(refined=False, prod=True):
        n_clusters = [num_clusters, num_refined_clusters][refined]
        if refined:
            refined = "refined_"
        else:
            refined = ""
        if prod:
            utility = "production"
        else:
            utility = "consumption"
        with open(f"./src/clustering_experiments/data/{initial_user}_rankings/{refined}clustering_{utility}_ranking.txt", "r") as f:
            lines = f.readlines()
            final_list = []  # List of top users for each cluster across each run
            top_users_run = []
            top_users_cluster = []
            for line in lines:
                line = line.strip()
                if line[0] == "-":
                    top_users_run.append(top_users_cluster)
                    final_list.append(top_users_run)
                    top_users_run = []
                    top_users_cluster = []
                elif line[0] == "*":
                    if top_users_cluster != []:
                        top_users_run.append(top_users_cluster)
                        top_users_cluster = []
                else:
                    top_users_cluster.append(line)
        return [sublist for sublist in final_list if len(sublist) == n_clusters][:runs]
    
    l = helper()
    list_users_prod_clusters = [[top_users_run[i] for top_users_run in l] for i in range(num_clusters)]  # List of top users across runs for each cluster
    for i, list_cluster in enumerate(list_users_prod_clusters):
        compare_top_users(list_cluster, title=f"Top 10 Users of Cluster {i} by Production Utility over {runs} runs", colour="pink", save=save, filename=f"t10_unrefined_{initial_user}_{i}")
    
    # l = helper(prod=False)
    # list_users_con_clusters = [[top_users_run[i] for top_users_run in l] for i in range(num_clusters)]  # List of top users across runs for each cluster
    # for i, list_cluster in enumerate(list_users_con_clusters):
    #     compare_top_users(list_cluster, title=f"Top 10 Users of Cluster {i} by Consumption Utility over {runs} runs", colour="purple")
    
    l = helper(refined=True)
    list_users_prod_refined_clusters = [[top_users_run[i] for top_users_run in l] for i in range(num_refined_clusters)]  # List of top users across runs for each cluster
    for i, list_cluster in enumerate(list_users_prod_refined_clusters):
        compare_top_users(list_cluster, title=f"Top 10 Users of Refined Cluster {i} by Production Utility over {runs} runs", colour="coral", save=save, filename=f"t10_refined_{initial_user}_{i}")
    
    # l = helper(refined=True, prod=False)
    # list_users_prod_refined_clusters = [[top_users_run[i] for top_users_run in l] for i in range(num_refined_clusters)]  # List of top users across runs for each cluster
    # for i, list_cluster in enumerate(list_users_prod_refined_clusters):
    #     compare_top_users(list_cluster, title=f"Top 10 Users of Refined Cluster {i} by Consumption Utility over {runs} runs", colour="red")


def compare_top_users(list_of_top_users_across_runs, title: str, n: int=10, colour="blue", save=False, filename="test"):
    """Compares the top n users across runs"""
    top_users_list = []
    for l in list_of_top_users_across_runs:
        top_users_list.extend(l)
    top_users_count = Counter(top_users_list).most_common(n)
    top_users, count = [user[0] for user in top_users_count], [user[1] for user in top_users_count]

    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot()
    ax.bar(top_users, count, color=colour)
    ax.set_xlabel("Top Users")
    ax.set_ylabel("Count across runs")
    ax.set_title(title)

    if save:
        plt.savefig(f'./src/clustering_experiments/data/img/{filename}')
    else:
        plt.show()


def compare_top_users_mongo(conn, user: str, threshold: int, discard_size: int):
    """Graphs top users for the clusters over runs for a particular threshold value and discard size value."""
    clusters_over_runs = non_discarded_clusters_over_runs(conn, threshold, discard_size)
    n = len(clusters_over_runs[0])
    print(n)
    # IMPORTANT: This assertion makes sure that the number of large (or non-discarded) clusters
    # is the same throughout all runs. If you have different numbers during each run
    # then an adapted version of this function may have to be created to compare similar runs. 
    assert all(len(clusters) == n for clusters in clusters_over_runs)  
    same_clusters_over_runs = [[clusters[i] for clusters in clusters_over_runs] for i in range(n)]
    for i, same_clusters in enumerate(same_clusters_over_runs):
        top_users_mongo_same_cluster(user, same_clusters, i, threshold)


def top_users_mongo_same_cluster(user: str, clusters: list, cluster_number: int, threshold: int):
    """Graphs the top 10 users of the same cluster over runs."""
    name_of_graph = f"Top Users of Cluster {cluster_number} of Threshold {threshold}"
    top_users_list = []
    for cluster in clusters:
        top_10_users = rank_users(user, cluster)[0]
        top_users_list.extend(top_10_users)
    top_users_count = Counter(top_users_list).most_common(10)
    top_users, count = [user[0] for user in top_users_count], [user[1] for user in top_users_count]
    average = [c/len(clusters) for c in count]

    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot()
    ax.bar(top_users, average, color="pink")
    ax.set_xlabel("Top Users")
    ax.set_ylabel("Average Occurences across runs")
    ax.set_title(name_of_graph)

    name_of_file = f"t10_refined_{user}_{threshold}_{cluster_number}"
    plt.savefig(f'./src/clustering_experiments/data/img/{name_of_file}.png')


def non_discarded_clusters_over_runs(conn, threshold: int, discard_size: int):
    """Returns clusters that are not discarded over runs"""
    collection = conn.ClusterTest.threshold
    clusters_over_runs = []
    for doc in collection.find({"threshold": threshold}):
        clusters = format_to_list_of_clusters(doc)
        non_discarded_clusters = discard_clusters_size_mongo(clusters, discard_size)
        clusters_over_runs.append(non_discarded_clusters)
    return clusters_over_runs


def discard_clusters_size_mongo(clusters, discard_size: int):
    """Returns the clusters in descending order of size after discarding clusters
    below a certain discard size.
    """
    non_discarded_clusters = []
    new_clusters = sorted(clusters, key=lambda c: len(c.users), reverse=True)
    for cluster in new_clusters:
        if len(cluster.users) >= discard_size:
            non_discarded_clusters.append(cluster)
    
    return non_discarded_clusters


if __name__ == "__main__":
    conn, db = connect_to_db()
    compare_top_users_mongo(conn, "timnitGebru", 0.4, 40)
    pass
