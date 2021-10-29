from collections import defaultdict
import src.scripts.create_social_graph_and_cluster as csgc
import numpy as np
from typing import List, Dict
from src.model.cluster import Cluster
from pymongo import MongoClient
from src.compare_clustering_algorithms import get_clusters
#need to import from compare_clustering_algorithms.py to generate data

def connect_to_db():
    try:
        conn = MongoClient()
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")
    # database
    db = conn.ClusterTest
    return conn, db


def generate_cluster_data():
    """store the clusters data in mongodb"""
    conn, db = connect_to_db()
    db = conn.ClusterTest
    c1, c2 = get_clusters("david_madras")
    rec_1 = format_cluster_to_doc(c1)
    rec_2 = format_cluster_to_doc(c2)

    # Insert doc into collections
    collection = db.unrefined
    collection.insert_one(rec_1)
    collection = db.refined
    collection.insert_one(rec_2)


def format_cluster_to_doc(clusters:List[Cluster])->Dict:
    """Format list of clusters to data in mongodb"""
    doc = {"clusters": [cluster.__dict__ for cluster in clusters],
           "num": len(clusters)}
    return doc


def get_all_data(refined=True):
    """Get list of data, each entry is experimental results for single cluster run"""
    all_data = []
    conn, db = connect_to_db()
    if refined:
        collection = db.refined
    else:
        collection = db.unrefined
    cursor = collection.find()
    for record in cursor:
        all_data.append(record)
    return all_data


def format_to_list_of_clusters(single_clustering_doc):
    """Given single data entry, return the list of users in each cluster"""
    cluster_list = []
    for cluster in single_clustering_doc["clusters"]:
        cluster_list.append(Cluster.fromDict(cluster))
    return cluster_list


def format_all_data(all_data):
    all_clusters = []
    for data_point in all_data:
        all_clusters.append(format_to_list_of_clusters(data_point))
    return all_clusters


if __name__ == "__main__":
    # generate cluster data and store in mongodb
    generate_cluster_data()


    all_data = get_all_data()
    # each datapoint is result from one clustering
    # each datapoint has 'num' and 'clusters'

    # this formats the data to list containing only clusters and users
    all_clusters = format_all_data(all_data)
    print(all_clusters)

