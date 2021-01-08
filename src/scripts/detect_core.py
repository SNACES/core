from src.activity.detect_core_activity import DetectCoreActivity
import argparse
import time
from src.scripts.parser.parse_config import parse_from_file
from src.shared.utils import get_project_root

DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/detect_core_config.yaml"


def detect_core(name: int, path=DEFAULT_PATH):
    config = parse_from_file(path)

    activity = DetectCoreActivity(config)
    activity.detect_core_by_screen_name(name)


if __name__ == "__main__":
    """
    Short script to download tweets
    """
    parser = argparse.ArgumentParser(description='Downloads the given number of tweets')
    parser.add_argument('-n', '--name', dest='name', required=True,
        help='The name of the user to start on', type=str)
    parser.add_argument('-p', '--path', dest='path', required=False,
        default=DEFAULT_PATH, help='The path of the config file', type=str)

    args = parser.parse_args()

    detect_core(args.name, args.path)
