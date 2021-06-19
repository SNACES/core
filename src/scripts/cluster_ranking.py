import argparse
import time
from src.dependencies.injector import Injector
from src.shared.utils import get_project_root
from src.shared.logger_factory import LoggerFactory

import json
import logging


log = LoggerFactory.logger(__name__, logging.ERROR)

DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/default_config.yaml"

def ranking(user_name: str, thresh, path=DEFAULT_PATH):

    injector = Injector.get_injector_from_file(path)
    process_module = injector.get_process_module()
    dao_module = injector.get_dao_module()

    local_followers_ranker = process_module.get_ranker("LocalFollowers")

    user_getter = dao_module.get_user_getter()

    seed_id = user_getter.get_user_by_screen_name(user_name).id
    type = 'local_and_global'
    filename = "./dc2_exp/" + str(type) + '/clusters_local_' + str(thresh) + '_global_50' '/' + str(user_name) + '_clusters_0.json'
    with open(filename, 'r') as file:
        user_lists = json.load(file)
        count = len(user_lists)

    for i in range(count): # Going through each cluster
        cluster = user_lists[i]
        log.info('Scoring Local Followers...')
        local_followers = local_followers_ranker.score_users(cluster)
        log.info(local_followers)
        ranked_followers = list(sorted(local_followers, key=local_followers.get, reverse=True))
        top15 = ranked_followers[:15]
        log.info(top15)

if __name__ == "__main__":
    """
    Short script to produce scatter plots
    """
parser = argparse.ArgumentParser(description='Short script to produce scatter plots of utility')

parser.add_argument('-n', '--screen_name', dest='name',
                    help="The screen name of the user to download", required=True)
parser.add_argument('-p', '--path', dest='path', required=False,
                    default=DEFAULT_PATH, help='The path of the config file', type=str)
parser.add_argument('-t', '--thresh', dest='thresh', required=False,
                    default=DEFAULT_PATH, help='thresh', type=float)

args = parser.parse_args()
ranking(args.name, args.thresh)
