from src.clustering_experiments.clustering_data import *
from pymongo import ASCENDING
from src.clustering_experiments.compare_clustering_algorithms import threshold_clusters
import matplotlib.pyplot as plt


def aggregate_same_threshhold(conn, threshold_vals):
    '''grab data from mongodb, average the number of clusters over experiments'''
    db = conn.ClusterTest
    count_list = []
    for threshold in threshold_vals:
        sum = 0
        count = 0
        for doc in db.threshold.find({"threshold": threshold}):
            doc['clusters'] = format_to_list_of_clusters(doc)
            sum += doc['num']
            count += 1
        count_list.append(sum / count)

    print(count_list)
    return count_list


def graph_count_list(x_vals, y_vals, fig_name):
    # colors = plt.get_cmap('Set1').colors
    fig, ax = plt.subplots()

    ax.plot(x_vals, y_vals)

    ax.set_title(f'Average Number of Clusters over 10 Experiment Runs')
    ax.set_ylabel(f'Number of Clusters')
    ax.set_xlabel('Threshold Value')

    plt.savefig(fig_name)
    plt.show()



if __name__ == "__main__":
    # generate cluster data and store in mongodb
    conn, db = connect_to_db()
    threshold_vals = [0.2, 0.3, 0.4, 0.5, 0.6]

    # Generates cluster with top_num in range(5, 55, 5),
    # Along with thresh_mult = range(0.05, 0.55, 00.5)
    count_list = aggregate_same_threshhold(conn, threshold_vals)
    graph_count_list(threshold_vals, count_list, fig_name="threshold_graph.png")
