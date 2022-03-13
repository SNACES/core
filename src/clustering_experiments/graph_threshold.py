from src.clustering_experiments.clustering_data import *
from pymongo import ASCENDING
from src.clustering_experiments.compare_clustering_algorithms import threshold_clusters
import matplotlib.pyplot as plt
import graph_ranking as gr
from src.shared.utils import get_project_root

DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/create_social_graph_and_cluster_config.yaml"


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

    ax.set_title(f'Average Number of Clusters over 10 Experiment Runs')
    ax.set_ylabel(f'Number of Clusters')
    ax.set_xlabel('Threshold Value')

    plt.savefig(fig_name)
    plt.show()


def aggregate_size_of_clusters(conn, user, threshold, one=False):
    db = conn.ClusterTest
    size_count_dict = {}
    count = 0

    if one:
        doc = db.threshold.find_one({"threshold": threshold, "user": user})
        count = 1
        size_count_dict = update_size_count_dict(size_count_dict, doc)
    else:
        for doc in db.threshold.find({"threshold": threshold, "user": user}):
            count += 1
            size_count_dict = update_size_count_dict(size_count_dict, doc)

    return size_count_dict, count


def update_size_count_dict(size_count_dict, doc):
    clusters = format_to_list_of_clusters(doc)
    for cluster in clusters:
        size = len(cluster.users)
        if size not in size_count_dict:
            size_count_dict[size] = 1
        else:
            size_count_dict[size] += 1
    return size_count_dict


def graph_size_of_clusters(conn, user, threshold, one=False):
    size_count_dict, count = \
        aggregate_size_of_clusters(conn, user, threshold, one)

    fig, ax = plt.subplots()
    count_list = [val / count for val in size_count_dict.values()]
    key_list = [str(size) for size in sorted(size_count_dict.keys())]
    ax.bar(key_list, count_list)

    ax.set_title(f'Number of Clusters for Each Size, threshold={threshold} -- user')
    ax.set_ylabel(f'Count of Cluster given Size')
    ax.set_xlabel('Size of clusters')

    plt.savefig(f"dist_of_clusters_sizes_{threshold}_{user}.png")
    plt.show()


def graph_overlap(user, overlap_threshold, selected_user=None):
    social_graph, local_neighbourhood = csgc.create_social_graph(user, path=DEFAULT_PATH)
    overlaps = []

    user_id = csgc.get_user_by_screen_name(user).id
    selected_user_id = None
    local_neighbourhood_users = local_neighbourhood.get_user_id_list()

    if selected_user:
        selected_user_id = csgc.get_user_by_screen_name(selected_user).id
        assert str(selected_user_id) in local_neighbourhood_users

    selected_user_overlap = None
    for curr_user in local_neighbourhood_users:
        if curr_user != str(user_id):
            friends = local_neighbourhood.get_user_friends(curr_user)
            overlaps.append(len(friends))
            if selected_user and \
                    curr_user == str(selected_user_id):
                selected_user_overlap = len(friends)

    N = len(local_neighbourhood_users)
    overlaps.sort(reverse=True)
    x_vals = list(range(N - 1))
    plt.figure()
    plt.plot(x_vals, overlaps, label="local following list")
    plt.plot(x_vals, [overlap_threshold for _ in range(N - 1)], label="local following list threhold")
    if selected_user:
        x_selected = len([o for o in overlaps if o > selected_user_overlap])
        plt.plot(x_selected, selected_user_overlap, 'go', label=selected_user)
    plt.xlabel("User")
    plt.ylabel("Number of Followers in Local Neighborhood")
    plt.legend()
    plt.savefig(f"overlaps_for_{user}.png")



if __name__ == "__main__":
    # generate cluster data and store in mongodb
    conn, db = connect_to_db()
    #threshold_vals = [0.2, 0.3, 0.4, 0.5, 0.6]


    #count_list = aggregate_same_threshold(conn, threshold_vals)
    #graph_count_list(threshold_vals, count_list, fig_name="threshold_graph.png")

    # graph_size_of_clusters(conn, 0.2)

    # graph_overlap("jps_astro", 4)
    graph_overlap("jps_astro", 4, "RoyalAstroSoc")


