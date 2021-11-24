from src.dependencies.injector import Injector
from src.shared.utils import get_project_root
from create_social_graph_and_cluster import get_user_by_screen_name


DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/create_social_graph_and_cluster_config.yaml"

def rank_users(user, cluster, n:int = 10, path=DEFAULT_PATH):
    """Returns the top n ranked users from the given cluster with the seed id as user's id."""
    user_id = get_user_by_screen_name(user).id
    injector = Injector.get_injector_from_file(path)
    process_module = injector.get_process_module()
    dao_module = injector.get_dao_module()
    user_getter = dao_module.get_user_getter()

    prod_ranker = process_module.get_ranker()
    con_ranker = process_module.get_ranker("Consumption")

    prod_ranking, prod = prod_ranker.rank(user_id, cluster)
    con_ranking, con = con_ranker.rank(user_id, cluster)
    
    prod_ranking_users = prod_ranking.get_all_ranked_user_ids()
    con_ranking_users = con_ranking.get_all_ranked_user_ids()

    intersection = set()

    i = 9
    top_prod = set(prod_ranking_users[:i])
    top_con = set(con_ranking_users[:i])
    while len(intersection) <= n and i < len(prod_ranking_users):
        top_prod.add(prod_ranking_users[i])
        top_con.add(con_ranking_users[i])
        intersection = top_prod.intersection(top_con)
        i += 1
    
    top_n_users_prod = [user_getter.get_user_by_id(id).screen_name for id in sorted(intersection, key=prod.get, reverse=True)][:n]
    top_n_users_cons = [user_getter.get_user_by_id(id).screen_name for id in sorted(intersection, key=con.get, reverse=True)][:n]

    return top_n_users_prod, top_n_users_cons





