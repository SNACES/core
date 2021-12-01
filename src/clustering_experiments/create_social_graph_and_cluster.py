from src.dependencies.injector import Injector
from src.shared.utils import get_project_root
from src.shared.logger_factory import LoggerFactory
from src.process.data_cleaning.data_cleaning_distributions import jaccard_similarity
from src.model.local_neighbourhood import LocalNeighbourhood
# Just for type signatures
from typing import List
from src.model.user import User
from src.model.social_graph.social_graph import SocialGraph
from src.model.cluster import Cluster
import matplotlib.pyplot as plt

log = LoggerFactory.logger(__name__)
DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/create_social_graph_and_cluster_config.yaml"


def create_social_graph(screen_name: str, path=DEFAULT_PATH) -> tuple:
    """Returns a social graph and the local neighbourhood of the user with screen_name constructed
    out of the data in the local mongodb database.
    """
    try:
        log.info("Creating a Social Graph:")
        injector = Injector.get_injector_from_file(path)
        process_module = injector.get_process_module()
        dao_module = injector.get_dao_module()

        user = get_user_by_screen_name(screen_name, path)
        local_neighbourhood_getter = dao_module.get_local_neighbourhood_getter()
        local_neighbourhood = local_neighbourhood_getter.get_local_neighbourhood(user.id)
        social_graph_constructor = process_module.get_social_graph_constructor()
        social_graph = social_graph_constructor.construct_social_graph_from_local_neighbourhood(user.id, local_neighbourhood)
        return social_graph, local_neighbourhood

    except Exception as e:
        log.exception(e)
        exit()


def refine_social_graph_jaccard(screen_name: str, social_graph: SocialGraph, \
                        local_neighbourhood: LocalNeighbourhood, top_num: int=10, \
                        thresh_multiplier: float=0.1, path=DEFAULT_PATH) -> SocialGraph:
    """Returns a social graph refined using Jaccard Set Similarity using the social graph and the screen name of the user."""
    injector = Injector.get_injector_from_file(path)
    process_module = injector.get_process_module()
    dao_module = injector.get_dao_module()
    user_friend_getter = dao_module.get_user_friend_getter()

    user_id = get_user_by_screen_name(screen_name).id
    user_list = local_neighbourhood.get_user_id_list()
    jaccard_sim = []

    for user in user_list:
        friends = local_neighbourhood.get_user_friends(user)
        for friend in friends:
            sim = jaccard_similarity(friends, local_neighbourhood.get_user_friends(str(friend)))
            jaccard_sim.append(sim)

    jaccard_sim.sort(reverse=True)
    #graph_list(jaccard_sim, None, "Jaccard Similarity", "all_jac_sim.png")
    if len(jaccard_sim) >= top_num:
        threshold = sum(jaccard_sim[:top_num]) / top_num * thresh_multiplier
    elif len(jaccard_sim) == 0:
        threshold = 0
    else:
        threshold = sum(jaccard_sim[:len(jaccard_sim)]) / len(jaccard_sim) * thresh_multiplier

    log.info("Refining by Jaccard Similarity:")
    friends_map = {}
    for user in user_list:
        friends = local_neighbourhood.get_user_friends(user)
        friends_map[user] = []
        for friend in friends:
            sim = jaccard_similarity(friends, local_neighbourhood.get_user_friends(str(friend)))
            if sim >= threshold:
                friends_map[user].append(friend)

    log.info("Setting Local Neighbourhood:")
    refined_local_neighbourhood = LocalNeighbourhood(str(user_id), None, friends_map)
    social_graph_constructor = process_module.get_social_graph_constructor()
    refined_social_graph = social_graph_constructor.construct_social_graph_from_local_neighbourhood(user_id, refined_local_neighbourhood)

    return refined_social_graph

# TO BE DELETED
def refine_social_graph_old(screen_name: str, social_graph: SocialGraph, \
                        local_neighbourhood: LocalNeighbourhood, top_num: int=10, \
                        thresh_multiplier: float=0.1, path=DEFAULT_PATH) -> SocialGraph:
    """Returns a social graph refined using Jaccard Set Similarity using the social graph and the screen name of the user."""
    log.info("Refining Friends List:")
    injector = Injector.get_injector_from_file(path)
    process_module = injector.get_process_module()
    dao_module = injector.get_dao_module()
    user_friend_getter = dao_module.get_user_friend_getter()

    user_id = get_user_by_screen_name(screen_name).id
    user_list = local_neighbourhood.get_user_id_list()
    friends_map = {}
    for user in user_list:
        friends_list = []
        # Friends are people that the user follows
        friends = local_neighbourhood.get_user_friends(user)

        # friend is str anyways, can remove str()
        for friend in friends:
            if user in local_neighbourhood.get_user_friends(str(friend)):
                friends_list.append(friend)
            if user == str(user_id):  # Why is this elif statement required?
                # Checks whether the user's friend also has the user as a friend
                if int(user) in user_friend_getter.get_user_friends_ids(str(friend)):
                    friends_list.append(friend)
        # Maps every user to all the friends that are friends with the user
        friends_map[user] = friends_list

    log.info("Refining by Jaccard Similarity:")
    for user in user_list:
        friends_list = friends_map[user]
        # Stores the jaccard similarities for each friend of the user
        similarities = {}
        for friend in friends_list:
            # Calculates the similarity between the user's friend list and the friend's friend list
            sim = jaccard_similarity(friends_list, friends_map[str(friend)])
            similarities[friend] = sim
        # Sorts the list of friends in descending order of similarity with the user
        sorted_users = sorted(similarities, key=similarities.get, reverse=True)
        top_sum = 0
        for top_user in sorted_users[:top_num]:
            top_sum += similarities[top_user]
        if len(sorted_users) >= top_num:
            thresh = thresh_multiplier * (top_sum / top_num)
        elif len(sorted_users) == 0:
            thresh = 0
        else:
            thresh = thresh_multiplier * (top_sum / len(sorted_users))

        # Binary search to find all users above threshold
        # if len(sorted_users) < 10:
        #     mid = len(sorted_users)
        # else:
        #     low, high = 0, len(sorted_users) - 1
        #     while low <= high:
        #         mid = (low + high) // 2
        #         user = sorted_users[i]
        #         if low == high or similarities[user] == thresh:
        #             break
        #         elif similarities[user] < thresh:
        #             low = mid + 1
        #         else:
        #             high = mid - 1
        # friends_map[user] = sorted_users[:mid]

        # Linear search to find all users above threshold
        index = len(sorted_users)
        for i in range(len(sorted_users)):
            user = sorted_users[i]
            if similarities[user] < thresh:
                index = i
                break
        friends_map[user] = sorted_users[:index]
    log.info("Setting Local Neighbourhood:")
    refined_local_neighbourhood = LocalNeighbourhood(str(user_id), None, friends_map)
    social_graph_constructor = process_module.get_social_graph_constructor()
    refined_social_graph = social_graph_constructor.construct_social_graph_from_local_neighbourhood(user_id, refined_local_neighbourhood)

    return refined_social_graph


def refine_social_graph_jaccard_with_friends(screen_name: str, social_graph: SocialGraph, \
                                local_neighbourhood: LocalNeighbourhood, threshold=0.5, path=DEFAULT_PATH) -> SocialGraph:
    """Returns a social graph refined using Jaccard Set Similarity using the social graph and the screen name of the user."""
    injector = Injector.get_injector_from_file(path)
    process_module = injector.get_process_module()
    dao_module = injector.get_dao_module()
    user_friend_getter = dao_module.get_user_friend_getter()

    user_id = get_user_by_screen_name(screen_name).id
    user_list = local_neighbourhood.get_user_id_list()
    jaccard_sim = []

    graph_user_following(user_list, local_neighbourhood)
    for user in user_list:
        friends = local_neighbourhood.get_user_friends(user)
        for friend in friends:
            sim = jaccard_similarity(friends, local_neighbourhood.get_user_friends(str(friend)))
            jaccard_sim.append(sim)

    jaccard_sim.sort(reverse=True)
    graph_list(jaccard_sim, None, "Jaccard Similarity", "all_jac_sim.png")
    graph_list(jaccard_sim[:100], None, "Jaccard Similarity", "top_jac_sim.png")

    log.info("Refining by Jaccard Similarity:")
    friends_map = {}
    for user in user_list:
        friends = local_neighbourhood.get_user_friends(user)
        friends_map[user] = []
        for friend in friends:
            sim = jaccard_similarity(friends, local_neighbourhood.get_user_friends(str(friend)))
            if sim >= threshold:
                friends_map[user].append(friend)

    log.info("Setting Local Neighbourhood:")
    refined_local_neighbourhood = LocalNeighbourhood(str(user_id), None, friends_map)
    social_graph_constructor = process_module.get_social_graph_constructor()
    refined_social_graph = social_graph_constructor.construct_social_graph_from_local_neighbourhood(user_id, refined_local_neighbourhood)

    return refined_social_graph


def clustering_from_social_graph(screen_name: str, social_graph: SocialGraph, path=DEFAULT_PATH) -> List[Cluster]:
    """Returns clusters from the social graph and screen name of user."""
    try:
        log.info("Clustering:")
        user = get_user_by_screen_name(screen_name, path)
        injector = Injector.get_injector_from_file(path)
        process_module = injector.get_process_module()
        dao_module = injector.get_dao_module()
        clusterer = process_module.get_clusterer()
        clusters = clusterer.cluster_by_social_graph(user.id, social_graph, None)
        return clusters
    except Exception as e:
        log.exception(e)
        exit()

def get_user_by_screen_name(screen_name: str, path=DEFAULT_PATH) -> User:
    """Returns a user object from their twitter screen name."""
    injector = Injector.get_injector_from_file(path)
    dao_module = injector.get_dao_module()
    user_getter = dao_module.get_user_getter()
    user = user_getter.get_user_by_screen_name(screen_name)
    return user


def graph_user_following(user_list, local_neighbourhood):
    friends_list_val = []
    for user in user_list:
        friends = local_neighbourhood.get_user_friends(user)
        friends_list_val.append(len(friends))
    friends_list_val.sort(reverse=True)
    graph_list(friends_list_val, "friends", "number of friends", "all_following.png")
    graph_list(friends_list_val[:10], "friends", "number of friends", "top_following.png")


def graph_list(y_val, x_label, y_label, fig_name):
    plt.figure()
    plt.plot(y_val)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(fig_name)



if __name__ == "__main__":
    # Play around with threshold multiplier and top num
    social_graph, local_neighbourhood = create_social_graph("timnitGebru")
    refined_social_graph = refine_social_graph_jaccard_with_friends("timnitGebru", social_graph, local_neighbourhood, threshold=0.5)
    # clusters = clustering_from_social_graph("david_madras", social_graph)
    refined_clusters = clustering_from_social_graph("timnitGebru", refined_social_graph)
