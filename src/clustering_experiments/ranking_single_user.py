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

DEFAULT_PATH = str(
    get_project_root()) + "/src/scripts/config/create_social_graph_and_cluster_config.yaml"


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


def non_discarded_clusters_over_runs(conn, threshold: int, discard_size: int):
    """Returns clusters that are not discarded over runs"""
    collection = conn.ClusterTest.threshold
    clusters_over_runs = []
    for doc in collection.find({"threshold": threshold}):
        clusters = format_to_list_of_clusters(doc)
        non_discarded_clusters = discard_clusters_size_mongo(clusters,
                                                             discard_size)
        clusters_over_runs.append(non_discarded_clusters)
    return clusters_over_runs


def rank_single_user(user, cluster, new_user, path=DEFAULT_PATH):
    """add the new_user to cluster of user, then return (production, consumption)
    of the new_user in that cluster"""
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

    # print(prod_ranker_scores)
    # print(con_ranker_scores)
    print(prod_ranker_scores[f'{new_user_id}'],
          con_ranker_scores[f'{new_user_id}'])
    return prod_ranker_scores[f'{new_user_id}'], con_ranker_scores[
        f'{new_user_id}']


def rank_single_user_from_data(conn, user: str, threshold: float,
                               discard_size: int, new_user):
    """For now this uses one single point of data instead aggregating over runs"""
    clusters = non_discarded_clusters_over_runs(conn, threshold, discard_size)[
        0]
    prods, cons, prod_norms, con_norms = [], [], [], []
    for i, cluster in enumerate(clusters):
        size = len(cluster.users) + 1
        prod, con = rank_single_user(user, cluster, new_user)
        prod_norm, con_norm = prod/size, con/size

        prods.append(prod)
        cons.append(con)
        prod_norms.append(prod_norm)
        con_norms.append(con_norm)

    return prods, cons, prod_norms, con_norms

def graph_cross_cluster_rankings(conn, user: str, threshold: float,
                                 discard_size: int, users_to_rank):
    ''' rank each users in users_to_rank in user's clusters
    '''
    x_labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    # change the nested lists if you have more clusters to rank in
    # ex. if three, [[], [], []]
    prod_list = [[], []]
    con_list = [[], []]
    prod_norm_list = [[], []]
    con_norm_list = [[], []]
    lists = [prod_list, con_list, prod_norm_list, con_norm_list]
    for new_user in users_to_rank:
        print(new_user)
        prods, cons, prod_norms, con_norms = rank_single_user_from_data(conn, user, threshold,
        discard_size, new_user)
        new_vals = [prods, cons, prod_norms, con_norms]

        for i in range(0, len(lists)):
            cur_list = lists[i]
            cur_vals = new_vals[i]
            for j in range(0, len(cur_list)):
                cur_list[j].append(cur_vals[j])

        print(lists)
    print(prod_list)
    print(con_list)
    print(prod_norm_list)
    print(con_norm_list)
    graph_cross_cluster_ranking(x_labels, prod_list, 'production utility', 'Production Utilities of Previous Top Users in New Clusters', 'prod_rank.png')
    print(con_list)
    graph_cross_cluster_ranking(x_labels, con_list, 'consumption utility', 'Consumption Utilities of Previous Top Users in New Clusters', 'con_rank.png')
    graph_cross_cluster_ranking(x_labels, prod_norm_list, 'production utility (normalized)', 'Production Utilities (Normalized) of Previous Top Users in New Clusters', 'prod_norm_rank.png')
    graph_cross_cluster_ranking(x_labels, con_norm_list, 'consumption utility (normalized)', 'Consumption Utilities (Normalized) of Previous Top Users in New Clusters', 'con_norm_rank.png')

    return 0

def graph_cross_cluster_ranking(x_vals, y_vals, y_label, fig_label, fig_name):
    '''helper function for creating a graph, where x_vals is user index,
    y_vals is nested list = [[vals_for_cluster0], [vals_for_cluster1], ..]'''
    x = np.arange(len(x_vals))  # the label locations
    width = 0.2  # the width of the bars

    fig, ax = plt.subplots()

    # Might have to changed the x-width stuffs for different number of bars
    rects1 = ax.bar(x - width/2, y_vals[0], width, label=f'Cluster {0}')
    ax.bar_label(rects1, padding=3)
    rects2 = ax.bar(x + width/2, y_vals[1], width, label=f'Cluster {1}')
    ax.bar_label(rects2, padding=3)
    print('here')
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(y_label)
    ax.set_title(fig_label)
    ax.set_xticks(x, x_vals)
    ax.legend()

    fig.tight_layout()
    plt.savefig(fig_name)
    plt.show()
    return 0


if __name__ == "__main__":
    conn, db = connect_to_db()
    # Note: need to have the clusters data for cur_user
    # 92501 in this example
    #rank_single_user_from_data(conn, "ak92501", 0.3, 80, "hardmaru")
    users_to_rank = ['hardmaru', 'weights_biases', 'suzatweet', 'DynamicWebPaige', 'l2k', 'bhutanisanyam1', 'osanseviero', 'mmbronstein', 'mervenoyann', 'ericjang11']
    graph_cross_cluster_rankings(conn, "ak92501", 0.3, 80, users_to_rank)
    pass
