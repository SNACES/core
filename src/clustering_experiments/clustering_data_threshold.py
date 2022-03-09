from collections import defaultdict
import src.clustering_experiments.create_social_graph_and_cluster as csgc
import numpy as np
from typing import List, Dict
from src.model.cluster import Cluster
from pymongo import MongoClient
from src.clustering_experiments.clustering_data import *

def get_threshold_clusters(initial_user: str, threshold) -> List[Cluster]:
    """Return clusters with threshold_multiplier and top_num"""
    social_graph, local_neighbourhood = csgc.create_social_graph(initial_user)
    refined_social_graph = csgc.refine_social_graph_jaccard_users(initial_user,
                                                                  social_graph,
                                                                  local_neighbourhood,
                                                                  threshold=threshold)
    refined_clusters = csgc.clustering_from_social_graph(initial_user, refined_social_graph)
    return refined_clusters


def generate_threshold_cluster_data(conn, user, threshold):
    db = conn.ClusterTest
    collection = db.threshold

    clusters = get_threshold_clusters(user, threshold)
    doc = {"clusters": [cluster.__dict__ for cluster in clusters],
           "num": len(clusters),
           "threshold": threshold,
           "user": user}
    collection.insert_one(doc)


if __name__ == "__main__":
    # generate cluster data and store in mongodb
    conn, db = connect_to_db()

    # Generates cluster with top_num in range(5, 55, 5),
    # Along with thresh_mult = range(0.05, 0.55, 00.5)
    generate_threshold_cluster_data(conn)