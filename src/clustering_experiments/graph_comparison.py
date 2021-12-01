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

if __name__ == "__main__":
    # compare_number_clusters_user("david_madras", runs=70)
    # compare_top_users_user("david_madras", runs=20, save=True)
    # compare_number_clusters_user("hardmaru", runs=20, save=True)
    # compare_top_users_user("hardmaru", runs=20, num_clusters=2, num_refined_clusters=2, save=True)
    # compare_number_clusters_user("tw_killian", runs=20, save=True)
    # compare_top_users_user("tw_killian", runs=20, num_clusters=2, num_refined_clusters=2, save=True)

    compare_number_clusters_user("timnitGebru", runs=20, save=True)
    compare_top_users_user("timnitGebru", runs=20, num_clusters=1, num_refined_clusters=2, save=True)
    pass
