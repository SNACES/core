import os
import sys

from src.activity.download_user_tweets_activity import DownloadUserTweetsActivity
import argparse
import time
from src.dependencies.injector import Injector
from src.shared.utils import get_project_root
from src.shared.logger_factory import LoggerFactory
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from src.model.local_neighbourhood import LocalNeighbourhood
import json
import logging
import random
import gc

log = LoggerFactory.logger(__name__, logging.ERROR)

DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/default_config.yaml"

def ranking_distribution(user_name: str, thresh, path=DEFAULT_PATH):

    injector = Injector.get_injector_from_file(path)
    process_module = injector.get_process_module()
    dao_module = injector.get_dao_module()

    production_ranker = process_module.get_ranker()
    consumption_ranker = process_module.get_ranker("Consumption")
    local_followers_ranker = process_module.get_ranker("LocalFollowers")

    user_getter = dao_module.get_user_getter()

    seed_id = user_getter.get_user_by_screen_name(user_name).id
    type = 'local_and_global'
    filename = "./dc2_exp/" + str(type) + '/clusters_local_' + str(thresh) + '_global_50' '/' + str(user_name) + '_clusters_0.json'
    with open(filename, 'r') as file:
        user_lists = json.load(file)
        count = len(user_lists)

    for i in range(count):

        cluster = user_lists[i]
        log.info(len(cluster))
        log.info('Scoring Consumption...')
        consumption = consumption_ranker.score_users(cluster)
        ranked_consumption = list(sorted(consumption, key=consumption.get, reverse=True))
        consumptions = [consumption[user] for user in ranked_consumption]

        log.info('Scoring Production...')
        production = production_ranker.score_users(cluster)
        ranked_production = list(sorted(production, key=production.get, reverse=True))
        productions = [production[user] for user in ranked_production]

        log.info('Scoring Local Followers...')
        local_followers = local_followers_ranker.score_users(cluster)
        log.info(local_followers)
        ranked_followers = list(sorted(local_followers, key=local_followers.get, reverse=True))
        followers = [local_followers[user] for user in ranked_followers]

        titles = ['Distribution of Consumption at Local Threshold '
                  + str(thresh) + ' for Cluster ' + str(i+1), 'Distribution of Production at Local Threshold '
                  + str(thresh) + ' for Cluster ' + str(i+1),
                  'Distribution of Local Followers at Local Threshold ' + str(thresh) + ' for Cluster ' + str(i+1)]

        title = titles[0]
        plt.bar(ranked_consumption, consumptions)
        plt.ylabel('Consumption Utility')
        plt.xlabel('Users in Cluster')
        plt.title(title)
        plt.show()

        title = titles[1]
        plt.bar(ranked_production, productions)
        plt.ylabel('Production Utility')
        plt.xlabel('Users in Cluster')
        plt.title(title)
        plt.show()

        title = titles[2]
        plt.bar(ranked_followers, followers)
        plt.ylabel('Local Followers')
        plt.xlabel('Users in Cluster')
        plt.title(title)
        plt.show()

        compare_top_users(ranked_consumption, ranked_production, ranked_followers, i+1, thresh, user_getter)


def compare_top_users(consumption, production, local_followers, cluster_num, thresh, user_getter):
    for i in range(1, 3):
        top_consumption = consumption[:5*i]
        top_production = production[:5*i]
        top_followers = local_followers[:5*i]
        # Take production to be reference set
        similarities = []
        consumption_sim = jaccard_similarity(top_production, top_consumption)
        similarities.append(consumption_sim)
        followers_sim = jaccard_similarity(top_production, top_followers)
        similarities.append(followers_sim)
        consumption_followers_sim = jaccard_similarity(top_consumption, top_followers)
        similarities.append(consumption_followers_sim)
        log.info(similarities)
        title = "Similarity of Top " + str(5*i) + " Users of Utility Functions for " \
                                                  "Cluster " + str(cluster_num) + " at Local Threshold " + str(thresh)
        plt.bar(['Consumption and Production', 'Local Followers and Production', 'Consumption and Local Followers' ], similarities)
        plt.ylabel('Jaccard Similarity')
        plt.xlabel('Utility Functions')
        plt.title(title)
        plt.show()

        top_consumption_names = [user.screen_name for user in user_getter.get_users_by_id_list(top_consumption)]
        log.info(top_consumption_names)
        top_production_names = [user.screen_name for user in user_getter.get_users_by_id_list(top_production)]
        log.info(top_production_names)
        top_followers_names = [user.screen_name for user in user_getter.get_users_by_id_list(top_followers)]
        log.info(top_followers_names)

def jaccard_similarity(user_list1, user_list2):
    intersection = len(list(set(user_list1).intersection(user_list2)))
    union = (len(user_list1) + len(user_list2)) - intersection

    return float(intersection) / union

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
    ranking_distribution(args.name, args.thresh)
