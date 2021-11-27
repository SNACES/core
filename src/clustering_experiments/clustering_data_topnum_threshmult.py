from collections import defaultdict
import src.clustering_experiments.create_social_graph_and_cluster as csgc
import numpy as np
from typing import List, Dict
from src.model.cluster import Cluster
from pymongo import MongoClient
from src.clustering_experiments.clustering_data import *

def get_threshold_clusters(initial_user: str, top_num: int=10, thresh_multiplier: float=0.1) -> List[Cluster]:
    """Return clusters with threshold_multiplier and top_num"""
    social_graph, local_neighbourhood = csgc.create_social_graph(initial_user)
    refined_social_graph = csgc.refine_social_graph_jaccard(initial_user, social_graph,
                                                    local_neighbourhood,
                                                    top_num=top_num,
                                                    thresh_multiplier=thresh_multiplier)
    refined_clusters = csgc.clustering_from_social_graph(initial_user, refined_social_graph)
    return refined_clusters


def generate_threshold_cluster_data(conn):
    db = conn.ClusterTest
    collection = db.threshold

    top_num_vals = [10, 100, 1000, 10000]
    thresh_mult_vals = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

    for top_num in top_num_vals:
        for thresh_mult in thresh_mult_vals:
            clusters = get_threshold_clusters("timnitGebru", top_num, thresh_mult)
            doc = {"clusters": [cluster.__dict__ for cluster in clusters],
                   "num": len(clusters),
                   "top_num": top_num,
                   "threshold_multiplier": thresh_mult}
            collection.insert_one(doc)


if __name__ == "__main__":
    # generate cluster data and store in mongodb
    conn, db = connect_to_db()

    # Generates cluster with top_num in range(5, 55, 5),
    # Along with thresh_mult = range(0.05, 0.55, 00.5)
    generate_threshold_cluster_data(conn)
