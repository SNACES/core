import argparse
import time
from src.dependencies.injector import Injector
from src.shared.utils import get_project_root
from src.shared.logger_factory import LoggerFactory
from typing import List

log = LoggerFactory.logger(__name__)

DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/detect_community_config.yaml"


def detect_community(name_list: List, path=DEFAULT_PATH):
    try:
        injector = Injector.get_injector_from_file(path)
        process_module = injector.get_process_module()

        community_detector = process_module.get_community_detector()
        community_detector.detect_community_by_screen_name(name_list)
    except Exception as e:
        log.exception(e)
        exit()


if __name__ == "__main__":
    """
    Short script to download tweets
    """
    parser = argparse.ArgumentParser(description='Detect community from seed sets')
    # parser.add_argument('-n', '--name', dest='name', required=True,
    #     help='The name of the user to start on', type=str)
    parser.add_argument('-n', '--name', dest='name', required=True, 
        type=str, nargs='*', help="The name of the user to start on")
    parser.add_argument('-p', '--path', dest='path', required=False,
        default=DEFAULT_PATH, help='The path of the config file', type=str)

    args = parser.parse_args()

    detect_community(args.name, args.path)