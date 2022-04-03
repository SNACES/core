from src.clustering_experiments.clustering_data import *
from pymongo import ASCENDING
from src.clustering_experiments.compare_clustering_algorithms import threshold_clusters
import matplotlib.pyplot as plt
import graph_ranking as gr
from src.shared.utils import get_project_root
import src.dependencies.injector as sdi

DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/create_social_graph_and_cluster_config.yaml"

def _get_selected_user_ids(selected_users, local_neighbourhood_users):
    selected_user_ids = []
    for selected_user in selected_users:
        selected_user_id = csgc.get_user_by_screen_name(selected_user).id
        assert str(selected_user_id) in local_neighbourhood_users
        selected_user_ids.append(str(selected_user_id))
    return selected_user_ids

def _graph_distribution_helper(ly_dict, ls):
    """ly_dict: labels to y_vals dict, ls: selected labels
    return the (x_vals, y_vals) for distribution and (xs, ys) for selected data
    """
    num = len(ly_dict.keys())

    x_vals = list(range(num))
    y_vals = list(ly_dict.values())
    y_vals.sort(reverse=True)

    xs = []
    ys = []

    if ls:
        for l in ls:
            y = ly_dict[l]
            x = len([val for val in y_vals if val > y])
            xs.append(x)
            ys.append(y)

    return x_vals, y_vals, xs, ys

def graph_local_following(user, selected_users=None, iter_num=False):
    social_graph, local_neighbourhood = csgc.create_social_graph(user, path=DEFAULT_PATH)
    local_following_dict = {}

    user_id = csgc.get_user_by_screen_name(user).id
    local_neighbourhood_users = local_neighbourhood.get_user_id_list()

    selected_user_ids = _get_selected_user_ids(selected_users, local_neighbourhood_users)

    for curr_user in local_neighbourhood_users:
        if curr_user != str(user_id):
            friends = local_neighbourhood.get_user_friends(curr_user)
            local_following_dict[str(curr_user)] = len(friends)
    local_following_dict[str(user_id)] = len(local_neighbourhood.get_user_friends(str(user_id)))

    x_vals, y_vals, xs, ys = _graph_distribution_helper(local_following_dict, selected_user_ids)
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, label="local following list", color="C0")
    # plt.plot(x_vals, [overlap_threshold for _ in range(N - 1)], label="local following list threhold")
    if selected_users:
        ax.scatter(xs, ys, color="C1")
        for i, txt in enumerate(selected_users):
            ax.annotate(txt, (xs[i], ys[i]))

    plt.xlabel("User")
    plt.ylabel("Number of Following in Local Neighborhood")
    plt.legend()
    if iter_num:
        plt.title(f"Distribution of Following for User -- {user}, Iter {iter_num}")
    else:
        plt.title(f"Distribution of Following for User -- {user}")
    plt.savefig(f"localfollowing_for_{user}.png")


def graph_local_follower(user, selected_users=None, iter_num=None):
    social_graph, local_neighbourhood = csgc.create_social_graph(user, path=DEFAULT_PATH)
    local_follower_dict = {}

    user_id = csgc.get_user_by_screen_name(user).id
    local_neighbourhood_users = local_neighbourhood.get_user_id_list()
    local_neighbourhood_users = [str(u) for u in local_neighbourhood_users]

    selected_user_ids = _get_selected_user_ids(selected_users, local_neighbourhood_users)
    selected_user_ids = [str(s) for s in selected_user_ids]

    injector = sdi.Injector.get_injector_from_file(DEFAULT_PATH)
    dao_module = injector.get_dao_module()
    user_friend_getter = dao_module.get_user_friend_getter()

    for curr_user in local_neighbourhood_users:
        # friends = local_neighbourhood.get_user_friends(curr_user)
        friends = user_friend_getter.get_user_friends_ids(str(curr_user))
        friends = [str(f) for f in friends]
        for friend in friends:
            if str(friend) not in local_neighbourhood_users:
                pass
            elif friend not in local_follower_dict:
                local_follower_dict[str(friend)] = 1
            else:
                local_follower_dict[str(friend)] += 1

    x_vals, y_vals, xs, ys = _graph_distribution_helper(local_follower_dict, selected_user_ids)

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, label="local follower list", color="C2")
    # plt.plot(x_vals, [overlap_threshold for _ in range(N - 1)], label="local following list threhold")
    if selected_users:
        ax.scatter(xs, ys, color="C1")
        for i, txt in enumerate(selected_users):
            ax.annotate(txt, (xs[i], ys[i]))

    plt.xlabel("User")
    plt.ylabel("Number of Followers in Local Neighborhood")
    plt.legend()
    if iter_num:
        plt.title(f"Distribution of Followers for User -- {user}, Iter {iter_num}")
    else:
        plt.title(f"Distribution of Followers for User -- {user}")
    plt.savefig(f"localfollower_for_{user}.png")


if __name__ == "__main__":
    graph_local_following("jps_astro", ["RoyalAstroSoc", "astrogrant"], iter_num=1)
    graph_local_follower("jps_astro", ["RoyalAstroSoc", "astrogrant"], iter_num=1)

    graph_local_following("RoyalAstroSoc", ["esa", "NASA"], iter_num=2)
    graph_local_follower("RoyalAstroSoc", ["esa", "NASA"], iter_num=2)

    graph_local_following("esa", ["NASAKennedy"], iter_num=3)
    graph_local_follower("esa", ["NASAKennedy"], iter_num=3)

    graph_local_following("NASAKennedy", ["NASAKennedy"], iter_num=4)
    graph_local_follower("NASAKennedy", ["NASAKennedy"], iter_num=4)

    # graph_local_following("Karen_Chess1", ["chess24com"], iter_num=1)
    # graph_local_follower("Karen_Chess1", ["chess24com"], iter_num=1)

    # graph_local_following("chess24com", ["chess24com"], iter_num=2)
    # graph_local_follower("chess24com", ["chess24com"], iter_num=2)
