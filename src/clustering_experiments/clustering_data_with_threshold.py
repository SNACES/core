from collections import defaultdict
import src.clustering_experiments.create_social_graph_and_cluster as csgc
import numpy as np
from typing import List, Dict
from src.model.cluster import Cluster
from pymongo import MongoClient
from src.clustering_experiments.clustering_data import *
from src.clustering_experiments.compare_clustering_algorithms import get_clusters

def get_threshold_clusters(initial_user: str, top_num: int=10, thresh_multiplier: float=0.1) -> List[Cluster]:
    """Return clusters with threshold_multiplier and top_num"""
    social_graph, local_neighbourhood = csgc.create_social_graph(initial_user)
    refined_social_graph = csgc.refine_social_graph(initial_user, social_graph,
                                                    local_neighbourhood,
                                                    top_num=top_num,
                                                    thresh_multiplier=thresh_multiplier)
    refined_clusters = csgc.clustering_from_social_graph(initial_user, refined_social_graph)
    return refined_clusters


def generate_threshold_cluster_data(db, conn):
    db = conn.ClusterTest
    collection = db.threshold

    for top_num in range(10, 50, 5):
        for i in range(1, 11):
            thresh_mult = 0.05*i
            clusters = get_threshold_clusters("david_madras", top_num, thresh_mult)
            doc = {"clusters": [cluster.__dict__ for cluster in clusters],
                   "num": len(clusters),
                   "top_num": top_num,
                   "threshold_multiplier": thresh_mult}
            collection.insert_one(doc)



if __name__ == "__main__":
    # generate cluster data and store in mongodb
    conn, db = connect_to_db()

    # Generates cluster with top_num in range(10, 50, 5),
    # Along with thresh_mult = range(0.05, 0.55, 0.0.5)
    generate_threshold_cluster_data(db, conn)
