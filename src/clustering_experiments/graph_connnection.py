from src.shared.utils import get_project_root
import src.dependencies.injector as sdi
import src.clustering_experiments.create_social_graph_and_cluster as csgc
import networkx as nx
import matplotlib.pyplot as plt

DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/create_social_graph_and_cluster_config.yaml"


def graph_connection(user: str, cluster, cluster_number: int, threshold: int, top_10_users):


    name_of_graph = f"Connection between Top Users of Cluster {cluster_number}, threshold {threshold} -- {user}, size {len(cluster.users)}"

    top_10_users = list.copy(top_10_users)

    user_id = csgc.get_user_by_screen_name(user).id

    injector = sdi.Injector.get_injector_from_file(DEFAULT_PATH)
    dao_module = injector.get_dao_module()
    user_friend_getter = dao_module.get_user_friend_getter()

    G = nx.DiGraph()
    user_id, top_10_user_ids = str(user_id), [str(csgc.get_user_by_screen_name(i).id) for i in top_10_users]
    if user_id in top_10_user_ids:
        top_10_user_ids.remove(user_id)
        top_10_users.remove(user)

    # add nodes to G
    for u in top_10_users:
        G.add_node(u)

    # add connections to G
    print(top_10_users)
    N = len(top_10_user_ids)
    for i in range(N):
        u = top_10_users[i]
        u_id = top_10_user_ids[i]
        for j in range(N):
            v = top_10_users[j]
            v_id = top_10_user_ids[j]
            u_follows = [str(w) for w in user_friend_getter.get_user_friends_ids(u_id)]
            #print(v_id, u_follows)
            if v_id in u_follows:
                G.add_edge(u, v)

    fig, ax = plt.subplots()
    nx.draw_circular(G, node_color='skyblue', edge_color="deepskyblue", with_labels=True, font_size=10)
    plt.axis("off")
    plt.title(name_of_graph)
    plt.margins(0.1)
    plt.savefig(f"connection_{user}_{threshold}_{cluster_number}.png")
    plt.show()

