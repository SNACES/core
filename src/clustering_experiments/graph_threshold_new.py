from bson import ObjectId

from src.clustering_experiments.clustering_data import *
from pymongo import ASCENDING
from src.clustering_experiments.compare_clustering_algorithms import threshold_clusters
import matplotlib.pyplot as plt


def aggregate_same_threshold(conn, threshold_vals):
    '''grab data from mongodb, average the number of clusters over experiments'''
    db = conn.ClusterTest
    count_list = []
    for threshold in threshold_vals:
        sum = 0
        count = 0
        for doc in db.threshold.find({"threshold": threshold}):
            sum += doc['num']
            count += 1
        count_list.append(sum / count)

    print(count_list)
    return count_list


def graph_count_list(x_vals, y_vals, fig_name):
    '''graphs the plot for average number of clusters across experiments'''
    # colors = plt.get_cmap('Set1').colors
    fig, ax = plt.subplots()

    ax.plot(x_vals, y_vals)

    ax.set_title(f'Average Number of Clusters over 20 Experiment Runs')
    ax.set_ylabel(f'Number of Clusters')
    ax.set_xlabel('Threshold Value')

    plt.savefig(fig_name)
    plt.show()


def aggregate_size_of_clusters(conn, threshold, one=False):
    '''grab data from mongodb, average the number of clusters over experiments'''
    db = conn.ClusterTest
    size_count_dict = {}
    count = 0

    #for doc in db.threshold.find({"top_num": 10, "threshold_multiplier": 0.5})
    #Just for test since I don't have new data yet -^-
    for doc in db.threshold.find({"threshold": threshold}):
        count += 1
        clusters = format_to_list_of_clusters(doc)
        for cluster in clusters:
            size = len(cluster.users)
            if size not in size_count_dict:
                size_count_dict[size] = 1
            else:
                size_count_dict[size] += 1
    return size_count_dict, count


def graph_size_of_clusters(conn, threshold):
    ''''''
    size_count_dict, count = aggregate_size_of_clusters(conn, threshold)

    fig, ax = plt.subplots()
    count_list = [val / count for val in size_count_dict.values()]
    #ax.bar(size_count_dict.keys(), count_list, )
    ax.hist(size_count_dict.keys(), bins=250, range=(0,250), weights=count_list)

    ax.set_title(f'Average Number of Clusters for Each Size, threshold={threshold}')
    ax.set_ylabel(f'Average Count of Cluster of Each Size')
    ax.set_xlabel('Size of clusters')

    plt.savefig(f"dist_of_clusters_sizes_threshold_{threshold}.png")
    plt.show()


def graph_size_of_clusters_bar(conn, threshold):
    ''''''
    size_count_dict, count = aggregate_size_of_clusters(conn, threshold)

    fig, ax = plt.subplots()

    x_list = []
    y_list = []
    for key in sorted(size_count_dict.keys(), reverse=False):
        x_list.append(f"{key}")
        y_list.append(size_count_dict[key]/count)

    ax.bar(x_list, y_list)

    ax.set_title(f'Average Number of Clusters for Each Size, threshold={threshold}')
    ax.set_ylabel(f'Average Count of Cluster of Each Size')
    ax.set_xlabel('Size of clusters')

    plt.savefig(f"bar_of_clusters_sizes_threshold_{threshold}.png")
    plt.show()



def graph_size_of_clusters_for_one(conn, threshold, id=False):
    db = conn.ClusterTest
    size_count_dict = {}
    count = 0

    if id:
        doc = db.threshold.find_one({"_id": ObjectId(id)})
    else:
        doc = db.threshold.find_one({"threshold": threshold})
    clusters = format_to_list_of_clusters(doc)
    for cluster in clusters:
        size = len(cluster.users)
        if size not in size_count_dict:
            size_count_dict[size] = 1
        else:
            size_count_dict[size] += 1

    fig, ax = plt.subplots()
    ax.hist(size_count_dict.keys(), bins=250, range=(0,250), weights=size_count_dict.values())

    ax.set_title(f'Count of Clusters given Size for single experiment, threshold={threshold}')
    ax.set_ylabel(f'Count')
    ax.set_xlabel('Size of clusters')

    if id:
        plt.savefig(f"one_dist_of_sizes_threshold_{threshold}_2.png")
    else:
        plt.savefig(f"one_dist_of_sizes_threshold_{threshold}.png")
    plt.show()

    fig, ax = plt.subplots()

    x_list = []
    y_list = []
    for key in sorted(size_count_dict.keys(), reverse=False):
        x_list.append(f"{key}")
        y_list.append(size_count_dict[key])

    ax.bar(x_list, y_list)

    ax.set_title(f'Count of Clusters given Size for single experiment, threshold={threshold}')
    ax.set_ylabel(f'Count')
    ax.set_xlabel('Size of clusters')

    if id:
        plt.savefig(f"one_bar_of_sizes_threshold_{threshold}_2.png")
    else:
        plt.savefig(f"one_bar_of_sizes_threshold_{threshold}.png")
    plt.show()





if __name__ == "__main__":
    # generate cluster data and store in mongodb
    conn, db = connect_to_db()

    # graph one of the clusters
    graph_size_of_clusters_for_one(conn, 0.5)

    # alternatively specify which data you want to graph by giving _id
    # graph_size_of_clusters_for_one(conn, 0.5, id="some number")
