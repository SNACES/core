# changed from from... import to prevent circular import
import src.dependencies.injector as sdi
from src.shared.utils import get_project_root
import src.clustering_experiments.create_social_graph_and_cluster as csgc


DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/create_social_graph_and_cluster_config.yaml"

def rank_users(user, cluster, path=DEFAULT_PATH):
    """Returns the top 10 ranked users from the given cluster with the seed id as user's id."""
    user_id = csgc.get_user_by_screen_name(user).id
    injector = sdi.Injector.get_injector_from_file(path)
    process_module = injector.get_process_module()
    dao_module = injector.get_dao_module()
    user_getter = dao_module.get_user_getter()

    prod_ranker = process_module.get_ranker()
    con_ranker = process_module.get_ranker("Consumption")
    infl1_ranker = process_module.get_ranker("InfluenceOne")
    infl2_ranker = process_module.get_ranker("InfluenceTwo")

    _, prod = prod_ranker.rank(user_id, cluster)
    _, con = con_ranker.rank(user_id, cluster)
    _, infl1 = infl1_ranker.rank(user_id, cluster)
    _, infl2 = infl2_ranker.rank(user_id, cluster)

    intersection_ranking = get_intersection_ranking(prod, con, infl1, infl2)

    top_n_users = [user_getter.get_user_by_id(id).screen_name for id in intersection_ranking]
    return top_n_users

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
    prod_ranking = sorted(prod.keys(), key=prod.get, reverse=True)
    con_ranking = sorted(con.keys(), key=con.get, reverse=True)
    infl1_ranking = sorted(infl1.keys(), key=infl1.get, reverse=True)
    infl2_ranking = sorted(infl2.keys(), key=infl2.get, reverse=True)
    top_all = {}
    for i in range(len(prod_ranking)):
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
                top_all[user] = i

        if len(intersection) >= 10: break

    return sorted(top_all.keys(), key=top_all.get)
