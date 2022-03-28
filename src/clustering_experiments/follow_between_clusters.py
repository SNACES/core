from collections import Counter
import create_social_graph_and_cluster as csgc
import matplotlib.pyplot as plt
from src.shared.utils import get_project_root
import src.dependencies.injector as sdi

DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/create_social_graph_and_cluster_config.yaml"

def graph_following_between_clusters(screen_name, c1, c2, c1_name="Cluster 1", c2_name="Cluster 2"):
    """Graphs the number of users from cluster 2 are being followed by each user from cluster 1
    sorted by production utility in decreasing order.
    """
    initial_user_id = csgc.get_user_by_screen_name(screen_name).id
    injector = sdi.Injector.get_injector_from_file(DEFAULT_PATH)
    process_module = injector.get_process_module()
    dao_module = injector.get_dao_module()

    user_friend_getter = dao_module.get_user_friend_getter()
    prod_ranker = process_module.get_ranker()
    
    prod_ranking, _ = prod_ranker.rank(initial_user_id, c1)
    # List of users in c1 sorted by production utility in descending order
    prod_ranking_users = prod_ranking.get_all_ranked_user_ids()

    c2_users = set(c2.users)
    c2_users.remove(str(initial_user_id))
    following_in_c2 = []
    for user_id in prod_ranking_users:
        if str(user_id) == str(initial_user_id):
            # so as to ignore spikes, we ignore the initial user
            # as it follows everyone in the local neighbourhood
            continue
        global_follows = {str(u) for u in user_friend_getter.get_user_friends_ids(str(user_id))}
        follows_in_c2 = c2_users.intersection(global_follows)
        follows_in_c2_count = len(follows_in_c2)
        following_in_c2.append(follows_in_c2_count)
    
    y_vals = following_in_c2
    x_vals = list(range(len(following_in_c2)))
    
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, color="magenta")
    ax.set_ylim([0, len(c2_users) - 1])
    plt.xlabel(f"Users from {c1_name} sorted by Production Utility")
    plt.ylabel(f"Number of Followers in {c2_name}")
    plt.title(f"Distribution of each user from {c1_name} following users from {c2_name}")
    plt.savefig(f"./src/clustering_experiments/data/info_flow/{screen_name}_{c1_name}_to_{c2_name}")
    # plt.show()


def graph_size_clusters(screen_name: str, clusters: list):
    """Graphs the clusters based on the size of clusters.
    Does not graph clusters below the discard_size.
    """
    fig, ax = plt.subplots()
    count_pairs = Counter(len(c.users) for c in clusters).most_common()
    count_pairs.sort(key=lambda c: c[0])
    y_vals = [c[1] for c in count_pairs]
    x_vals = [str(c[0]) for c in count_pairs]
    ax.bar(x_vals, y_vals)
    plt.title("Number of Clusters for Each Size, threshold=0.3")
    plt.ylabel("Count of Clusters of Each Size")
    plt.xlabel("Size of clusters")

    plt.savefig(f"./src/clustering_experiments/data/info_flow/{screen_name}_size_clusters")
    # plt.show()


if __name__ == "__main__":
    screen_name = "timnitGebru"
    threshold = 0.3
    user_id = csgc.get_user_by_screen_name(screen_name).id
    social_graph, local_neighbourhood = csgc.create_social_graph(screen_name)
    refined_social_graph = csgc.refine_social_graph_jaccard_users(screen_name, social_graph, local_neighbourhood, threshold=threshold)
    refined_clusters = csgc.clustering_from_social_graph(screen_name, refined_social_graph)
    sorted_clusters = sorted(refined_clusters, key=lambda c: len(c.users), reverse=True)

    # graph_size_clusters(screen_name, sorted_clusters)
    for i in range(5):
        for j in range(i + 1, 5):
            graph_following_between_clusters(screen_name, sorted_clusters[i], sorted_clusters[j], f"Cluster {i}", f"Cluster {j}")
            graph_following_between_clusters(screen_name, sorted_clusters[j], sorted_clusters[i], f"Cluster {j}", f"Cluster {i}")
