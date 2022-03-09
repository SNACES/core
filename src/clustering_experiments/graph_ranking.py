from collections import Counter
import matplotlib.pyplot as plt
from src.shared.utils import get_project_root
from src.clustering_experiments.clustering_data import *
from bson import ObjectId
from src.dependencies.injector import Injector
from src.shared.utils import get_project_root
from create_social_graph_and_cluster import get_user_by_screen_name
import numpy as np
from ranking_users_in_clusters import rank_users


DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/create_social_graph_and_cluster_config.yaml"


def graph_single_production(user: str, cluster, cluster_number: int, threshold: int):
    """Graphs the top 10 users of the same cluster over runs."""
    name_of_graph = f"Top Users of Cluster {cluster_number}, size  of Threshold {threshold}"

    top_10_users, top_10_values = rank_users(user, cluster)
    print(top_10_users)

    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot()
    ax.bar(top_10_users, top_10_values, color="pink")
    ax.set_xlabel("Top Users")
    ax.set_ylabel("Production Utility (number of followers)")
    ax.set_title(name_of_graph)

    name_of_file = f"t10_refined_{user}_{threshold}_{cluster_number}"
    plt.savefig(f'{str(get_project_root())}/src/clustering_experiments/data/img/{name_of_file}.png')


def compare_top_users_mongo_single(conn, user, threshold, discard_size, data_id=False):
    db = conn.ClusterTest
    user_id = get_user_by_screen_name(user).id
    if data_id:
        doc = db.threshold.find_one({"_id": ObjectId(data_id)})
    else:
        doc = db.threshold.find_one({"threshold": threshold, "user": user})
    clusters = format_to_list_of_clusters(doc)
    clusters_nested = []
    new_clusters = sorted(clusters, key=lambda c: len(c.users), reverse=False)
    for cluster in new_clusters:
        if len(cluster.users) >= discard_size:
            clusters_nested.append(cluster)
    for i, cluster in enumerate(clusters_nested):
        graph_utility(user, cluster, i, threshold)
    return clusters


def rank_users(user, cluster, n:int = 10, path=DEFAULT_PATH):
    """Returns the top n ranked users from the given cluster with the seed id as user's id."""
    user_id = get_user_by_screen_name(user).id
    injector = Injector.get_injector_from_file(path)
    process_module = injector.get_process_module()
    dao_module = injector.get_dao_module()
    user_getter = dao_module.get_user_getter()

    prod_ranker = process_module.get_ranker()
    con_ranker = process_module.get_ranker("Consumption")

    prod_ranking, prod = prod_ranker.rank(user_id, cluster)
    con_ranking, con = con_ranker.rank(user_id, cluster)

    prod_ranking_users = prod_ranking.get_all_ranked_user_ids()
    con_ranking_users = con_ranking.get_all_ranked_user_ids()

    intersection = set()

    i = 9
    top_prod = set(prod_ranking_users[:i])
    top_con = set(con_ranking_users[:i])
    intersection = top_prod.intersection(top_con)
    while len(intersection) <= n and i < len(prod_ranking_users):
        top_prod.add(prod_ranking_users[i])
        top_con.add(con_ranking_users[i])
        intersection = top_prod.intersection(top_con)
        i += 1

    top_n_users_id = sorted(intersection, key=prod.get, reverse=True)
    top_n_users_prod = [user_getter.get_user_by_id(user_id).screen_name for user_id in top_n_users_id]
    top_n_users_prod_value = [prod.get(user_id) for user_id in top_n_users_id]
    top_n_users_con_value = [con.get(user_id) for user_id in top_n_users_id]
    print(top_n_users_prod, top_n_users_prod_value, top_n_users_con_value)
    return top_n_users_prod, top_n_users_prod_value, top_n_users_con_value


def rank_single_user(user, cluster, new_user, path=DEFAULT_PATH):
    user_id = get_user_by_screen_name(user).id
    new_user_id = get_user_by_screen_name(new_user).id
    injector = Injector.get_injector_from_file(path)
    process_module = injector.get_process_module()
    dao_module = injector.get_dao_module()
    user_getter = dao_module.get_user_getter()

    prod_ranker = process_module.get_ranker()
    con_ranker = process_module.get_ranker("Consumption")
    user_ids = cluster.users
    user_ids.append(new_user_id)

    prod_ranker_scores = prod_ranker.score_users(user_ids)
    con_ranker_scores = con_ranker.score_users(user_ids)

    #print(prod_ranker_scores)
    #print(con_ranker_scores)
    print(prod_ranker_scores[f'{new_user_id}'], con_ranker_scores[f'{new_user_id}'])
    return prod_ranker_scores[f'{new_user_id}'], con_ranker_scores[f'{new_user_id}']


def rank_single_user_from_data(conn, user: str, threshold: float, discard_size: int, new_user):
    clusters = non_discarded_clusters_over_runs(conn, threshold, discard_size, user)[0]
    for i, cluster in enumerate(clusters):
        rank_single_user(user, cluster, new_user)

def compare_top_users_mongo(conn, user: str, threshold: float, discard_size: int, n):
    """Graphs top users for the clusters over runs for a particular threshold value and discard size value."""
    clusters_over_runs_diff = non_discarded_clusters_over_runs(conn, threshold, discard_size, user)
    clusters_over_runs = [clusters for clusters in clusters_over_runs_diff if len(clusters) == n]
    # IMPORTANT: This assertion makes sure that the number of large (or non-discarded) clusters
    # is the same throughout all runs. If you have different numbers during each run
    # then an adapted version of this function may have to be created to compare similar runs.
    # assert all(len(clusters) == n for clusters in clusters_over_runs)
    same_clusters_over_runs = [[clusters[i] for clusters in clusters_over_runs] for i in range(n)]
    for i, same_clusters in enumerate(same_clusters_over_runs):
        top_users_mongo_same_cluster(user, same_clusters, i, threshold)


def top_users_mongo_same_cluster(user: str, clusters: list, cluster_number: int, threshold: int):
    """Graphs the top 10 users of the same cluster over runs."""
    name_of_graph = f"Top Users of Cluster {cluster_number} of Threshold {threshold} Over {len(clusters)} Runs, with Average Size"
    top_users_list = []
    clusters_size_list = []
    for cluster in clusters:
        top_10_users = rank_users(user, cluster)[0]
        top_users_list.extend(top_10_users)
        clusters_size_list.append(len(cluster.users))
    clusters_size_arr = np.array(clusters_size_list)
    mean = round(np.mean(clusters_size_arr), 1)
    std = round(np.std(clusters_size_arr), 1)
    name_of_graph = f"Top Users of Additional Cluster of Threshold {threshold} Over {len(clusters)} Runs," \
                    f" with Mean Size {mean}, Std {std}"
    top_users_count = Counter(top_users_list).most_common(10)
    top_users, count = [user[0] for user in top_users_count], [user[1] for user in top_users_count]
    average = [c/len(clusters) for c in count]

    fig = plt.figure(figsize=(15, 7.5))
    ax = fig.add_subplot()
    ax.bar(top_users, average, color="pink")
    ax.set_xlabel("Top Users", fontsize=15)
    ax.set_ylabel("Average Occurrences across runs", fontsize=15)
    ax.set_title(name_of_graph, fontsize=20)

    name_of_file = f"t10_refined_{user}_{threshold}_{cluster_number}"
    plt.savefig(f'{str(get_project_root())}/src/clustering_experiments/data/img/{name_of_file}.png')


def non_discarded_clusters_over_runs(conn, threshold: int, discard_size: int, user="NLN"):
    """Returns clusters that are not discarded over runs"""
    collection = conn.ClusterTest.threshold
    clusters_over_runs = []
    for doc in collection.find({"threshold": threshold, "user": user}):
        clusters = format_to_list_of_clusters(doc)
        non_discarded_clusters = discard_clusters_size_mongo(clusters, discard_size)
        clusters_over_runs.append(non_discarded_clusters)
    return clusters_over_runs


def discard_clusters_size_mongo(clusters, discard_size: int):
    """Returns the clusters in descending order of size after discarding clusters
    below a certain discard size.
    """
    non_discarded_clusters = []
    new_clusters = sorted(clusters, key=lambda c: len(c.users), reverse=False)
    for cluster in new_clusters:
        if len(cluster.users) >= discard_size:
            non_discarded_clusters.append(cluster)

    return non_discarded_clusters


def graph_utility(user: str, cluster, cluster_number: int, threshold: int):
    """Graphs the top 10 users of the same cluster over runs."""
    name_of_graph = f"Top Users of Cluster {cluster_number}, threshold {threshold} -- {user}"

    top_10_users, top_10_prod, top_10_con = rank_users(user, cluster)

    fig = plt.figure(figsize=(18, 10))
    ax = fig.add_subplot()
    x = np.arange(len(top_10_users))  # the label locations
    width = 0.35  # the width of the bars

    rects1 = ax.bar(x - width/2, top_10_prod, width=width, color="orangered", label="production")
    rects2 = ax.bar(x + width/2, top_10_con, width=width, color="orange", label="consumption")
    ax.set_xlabel("Top Users")
    ax.set_ylabel("Utility")
    ax.set_xticks(x, top_10_users)
    ax.legend()

    ax.bar_label(rects1, padding=5)
    ax.bar_label(rects2, padding=5)

    ax.set_title(name_of_graph)

    name_of_file = f"t10_refined_{user}_{threshold}_{cluster_number}"
    plt.savefig(f'{str(get_project_root())}/src/clustering_experiments/data/img/{name_of_file}.png')


if __name__ == "__main__":
    conn, db = connect_to_db()
    # compare_top_users_mongo(conn, "timnitGebru", 0.2, 75, 3)

    #["hardmaru", "david\_madras", "timnitGebru"] respectively are [0.33, 0.349, 0.268].
    # print("hardmaru")
    # compare_top_users_mongo_single(conn, "hardmaru", 0.33, 70)
    #
    # print("david_madras")
    # compare_top_users_mongo_single(conn, "david_madras", 0.349, 70)

    print("specolations")
    compare_top_users_mongo_single(conn, "k", 0.2, 70)
    #compare_top_users_mongo_single(conn, "timnitGebru", 0.2, 75, data_id="61a6d1bb51f85b282efbfdf5")
    #compare_top_users_mongo_single(conn, "timnitGebru", 0.2, 75, data_id="61a6d1aff0116abddf8ad5fc")
    #compare_top_users_mongo_single(conn, "timnitGebru", 0.3, 50, data_id="61a6d1d59caf8da414f0d4b7")
    # print("Hardmaru")
    # print(rank_single_user_from_data(conn, "timnitGebru", 0.3, 60, "hardmaru"))
    # print("timnitGebru")
    # print(rank_single_user_from_data(conn, "timnitGebru", 0.3, 60, "timnitGebru"))
    #print(rank_single_user_from_data(conn, "timnitGebru", 0.3, 60, "fchoilet"))
    #print(rank_single_user_from_data(conn, "timnitGebru", 0.3, 60, "mer_edith"))
    #print(rank_single_user_from_data(conn, "timnitGebru", 0.3, 60, "_rockt"))
    # print("julien_c")
    # print(rank_single_user_from_data(conn, "timnitGebru", 0.3, 70, "julien_c"))
    #print(rank_single_user_from_data(conn, "timnitGebru", 0.3, 60, "mark_neidi"))
    pass
