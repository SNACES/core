import argparse
import os
import time

from src.scripts.cluster_ranking_experiments import jaccard_similarity
from src.dependencies.injector import Injector
from src.shared.utils import get_project_root
from src.shared.logger_factory import LoggerFactory

import json
import logging


log = LoggerFactory.logger(__name__, logging.ERROR)

DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/default_config.yaml"

def ranking(user_name: str, path=DEFAULT_PATH):

    injector = Injector.get_injector_from_file(path)
    process_module = injector.get_process_module()
    dao_module = injector.get_dao_module()

    local_followers_ranker = process_module.get_ranker("LocalFollowers")
    consumption_ranker = process_module.get_ranker("Consumption")
    production_ranker = process_module.get_ranker()

    user_getter = dao_module.get_user_getter()
    ranking_getter = dao_module.get_ranking_getter()

    cluster_getter = dao_module.get_cluster_getter()
    seed_id = user_getter.get_user_by_screen_name(user_name).id

    clusters, _ = cluster_getter.get_clusters(seed_id, params={"graph_type": "union"})

    production_ranking = ranking_getter.get_ranking(seed_id)
    cluster = clusters[1].users

    log.info('Scoring Consumption...')
    #consumption = consumption_ranker.score_users(cluster)
    #ranked_consumption = list(sorted(consumption, key=consumption.get, reverse=True))[:20]

    ranked_consumption = ['109117316', '1203825050476072960', '359831209', '1294363908694827010', '2492917412',
     '1291153576455266304', '929791330519322624', '2999992556', '254201259', '810582380', '66999485', '918511183', '161455525',
     '432957426', '6466252', '166479009', '748528569064710145', '382376904', '24223629', '2311193425']

    log.info('Scoring Production...')

    ranked_production = production_ranking.get_top_20_user_ids()
    consumption_users = [user_getter.get_user_by_id(str(id)).screen_name for id in ranked_consumption]
    production_users = [user_getter.get_user_by_id(str(id)).screen_name for id in ranked_production]
    log.info(consumption_users)
    log.info(production_users)
    log.info(len(set(consumption_users).intersection(production_users)))
    log.info(jaccard_similarity(ranked_consumption, ranked_production))




if __name__ == "__main__":
    """
    Short script to produce scatter plots
    """
parser = argparse.ArgumentParser(description='Short script to save rankings')

parser.add_argument('-n', '--screen_name', dest='name',
                    help="The screen name of the user to download", required=True)
parser.add_argument('-p', '--path', dest='path', required=False,
                    default=DEFAULT_PATH, help='The path of the config file', type=str)


args = parser.parse_args()
ranking(args.name)
