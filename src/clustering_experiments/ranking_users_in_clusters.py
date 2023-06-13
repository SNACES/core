# changed from from... import to prevent circular import
import src.dependencies.injector as sdi
from src.shared.utils import get_project_root
from src.model.cluster import Cluster
import src.clustering_experiments.create_social_graph_and_cluster as csgc
import src.clustering_experiments.build_cluster_tree as bct
import src.model.cluster_tree as ct
DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/create_social_graph_and_cluster_config.yaml"

def rank_users(user, cluster, path=DEFAULT_PATH):
    """Returns the top 10 ranked users from the given cluster with the seed id as user's id."""
    user_id = csgc.get_user_by_screen_name(user).id
    injector = sdi.Injector.get_injector_from_file(path)
    process_module = injector.get_process_module()
    dao_module = injector.get_dao_module()
    user_getter = dao_module.get_user_getter()

    # prod_ranker = process_module.get_ranker()
    # con_ranker = process_module.get_ranker("Consumption")
    sosu_ranker = process_module.get_ranker("SocialSupport")
    infl1_ranker = process_module.get_ranker("InfluenceOne")
    infl2_ranker = process_module.get_ranker("InfluenceTwo")

    # Second argument is the return of score_users
    # prod_rank, prod = prod_ranker.rank(user_id, cluster)
    # con_rank, con = con_ranker.rank(user_id, cluster)
    sosu_rank, sosu = sosu_ranker.rank(user_id, cluster)
    infl1_rank, infl1 = infl1_ranker.rank(user_id, cluster)
    infl2_rank, infl2 = infl2_ranker.rank(user_id, cluster)

    # intersection_ranking = get_intersection_ranking(prod, con, infl1, infl2)
    intersection_ranking = get_new_intersection_ranking(sosu, infl1)

    top_n_users = [user_getter.get_user_by_id(id).screen_name for id in intersection_ranking]
    # top_n_users = filter_user_by_clustering(intersection_ranking, "fchollet", user_getter)
    return top_n_users

def filter_user_by_clustering(intersection_ranking, screen_name, user_getter):
    thresh = 0.3
    base_user = intersection_ranking[0]
    cluster = Cluster(base_user, intersection_ranking)
    cur_node = ct.ClusterNode(0.3, cluster)
    soc_graph, neighbourhood = csgc.create_social_graph(screen_name)
    refined_soc_graph = \
        csgc.refine_social_graph_jaccard_users(screen_name, soc_graph,
                                               neighbourhood, threshold=thresh)
    cluster_neighbourhood, cluster_soc_graph, base_user_friends = \
        bct.generate_soc_graph_and_neighbourhood_from_cluster(cur_node,
                                                              neighbourhood)
    refined_cluster_soc_graph = \
        csgc.refine_social_graph_jaccard_users(base_user, cluster_soc_graph,
                                               cluster_neighbourhood,
                                               threshold=thresh)
    cluster_neighbourhood.users[str(cur_node.root.base_user)] = base_user_friends
    while True:
        child_nodes = bct.generate_clusters(user_getter.get_user_by_id(base_user).screen_name, refined_cluster_soc_graph,
                                        cluster_neighbourhood,
                                        thresh + 0.05, 0.05, thresh + 0.05)
        top = [-1, -1]
        for node in child_nodes:
            if len(node.root.users) > top[0]:
                top = (len(node.root.users), node)
        if top[0] < 10:
            top_n_users = [user_getter.get_user_by_id(id).screen_name for id in cur_node.root.users]
            return top_n_users
        cur_node = top[1]
        thresh += 0.05
        cluster_neighbourhood, cluster_soc_graph, base_user_friends = \
            bct.generate_soc_graph_and_neighbourhood_from_cluster(cur_node,
                                                              cluster_neighbourhood)
        refined_cluster_soc_graph = \
            csgc.refine_social_graph_jaccard_users(base_user, cluster_soc_graph,
                                                   cluster_neighbourhood,
                                                   threshold=thresh)
        cluster_neighbourhood.users[str(cur_node.root.base_user)] = base_user_friends

def get_new_intersection_ranking(sosu, infl1):
    """Produces a ranking that aggregates the Social Support and Influence One rankings

    Args:
        sosu, infl1:
            Is a dictionary where the key is the user id and the value is their
            score for the respective ranker
    Returns:
        An ordered list of about 10 highest ranked users sorted by highest rank.
    """
    # Get top 20 users from sosu_ranking
    sosu_ranking = list(sorted(sosu, key=lambda x: (sosu[x][0], sosu[x][1]), reverse=True))[:20]
    infl1_ranking = list(sorted(sosu, key=lambda x: (infl1[x][0], infl1[x][1]), reverse=False))
    # Lowest infl1 scores appear first
    
    # Remove lowest infl1_ranking users from sosu_ranking until 10 users are left
    for user in infl1_ranking:
        if user in sosu_ranking:
            sosu_ranking.remove(user)
        if len(sosu_ranking) <= 10:
            break
    return sosu_ranking

def get_intersection_ranking(prod, con, infl1, infl2):
    """Produces a ranking that is the intersection of the Production,
    Consumption, Influence One, and Influence Two rankings

    Args:
        prod, con, infl1, infl2:
            Are dictionaries where the key is the user id and the value is their
            score for the respective ranker
    Returns:
        An ordered list of about 10 highest ranked users sorted by highest rank.
    """
    prod_ranking = list(sorted(prod, key=lambda x: (prod[x][0], prod[x][1]), reverse=True))
    con_ranking = list(sorted(prod, key=lambda x: (con[x][0], con[x][1]), reverse=True))
    infl1_ranking = list(sorted(prod, key=lambda x: (infl1[x][0], infl1[x][1]), reverse=True))
    infl2_ranking = list(sorted(prod, key=lambda x: (infl2[x][0], infl2[x][1]), reverse=True))
    top_all = {}
    for i in range(1, len(prod_ranking) + 1):
        top_prod = set(prod_ranking[:i])
        top_con = set(con_ranking[:i])
        top_infl1 = set(infl1_ranking[:i])
        top_infl2 = set(infl2_ranking[:i])
        intersection = top_prod.intersection(
            top_con).intersection(
            top_infl1).intersection(
            top_infl2)

        for user in intersection:
            if user not in top_all:
                top_all[user] = [i, infl2_ranking.index(user)]

        #if len(intersection) >= 20: break
        if len(intersection) >= 10: break

    return sorted(top_all, key=lambda x: (top_all[x][0], top_all[x][1]))
