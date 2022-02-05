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
    for i, cluster in enumerate(clusters):
        rank_single_user(user, cluster, new_user)


if __name__ == "__main__":
    conn, db = connect_to_db()
    # Note: need to download data for those users before we can do the ranking
    print("Hardmaru")
    rank_single_user_from_data(conn, "timnitGebru", 0.3, 80, "hardmaru")
    print("timnitGebru")
    rank_single_user_from_data(conn, "timnitGebru", 0.3, 80, "timnitGebru")
    print("mmitchell_ai")
    print(rank_single_user_from_data(conn, "timnitGebru", 0.3, 60, "mmitchell_ai"))
    print("mer__edith")
    print(rank_single_user_from_data(conn, "timnitGebru", 0.3, 80, "mer__edith"))
    print("ak92501")
    print(rank_single_user_from_data(conn, "timnitGebru", 0.3, 60, "ak92501"))
    print("Abebab")
    rank_single_user_from_data(conn, "timnitGebru", 0.3, 80, "Abebab")
    print("julien_c")
    rank_single_user_from_data(conn, "timnitGebru", 0.3, 80, "julien_c")
    print("weights_biases")
    rank_single_user_from_data(conn, "timnitGebru", 0.3, 80, "weights_biases")
    print("DynamicWebPaige")
    rank_single_user_from_data(conn, "timnitGebru", 0.3, 80, "DynamicWebPaige")
    print("cdixon")
    rank_single_user_from_data(conn, "timnitGebru", 0.3, 80, "cdixon")
    pass
