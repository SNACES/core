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

def process_dates(path=DEFAULT_PATH):

    injector = Injector.get_injector_from_file(path)
    process_module = injector.get_process_module()
    dao_module = injector.get_dao_module()
    user_tweet_getter = dao_module.get_user_tweet_getter()
    user_tweet_getter.convert_dates()

if __name__ == "__main__":
    """
    Short script to process tweets
    """
    parser = argparse.ArgumentParser(description='Processes the given tweet')

    parser.add_argument('-p', '--path', dest='path', required=False,
                        default=DEFAULT_PATH, help='The path of the config file', type=str)

    args = parser.parse_args()

    process_dates(args.path)
