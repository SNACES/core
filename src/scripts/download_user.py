from src.activity.download_user_activity import DownloadUserActivity
import argparse
import time
from src.scripts.parser.parse_config import parse_from_file
from src.shared.utils import get_project_root

DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/download_user_config.yaml"


def download_user(name: str, path=DEFAULT_PATH):
    config = parse_from_file(path)

    activity = DownloadUserActivity(config)
    activity.download_user_by_screen_name(name)


if __name__ == "__main__":
    """
    Short script to download users
    """
    parser = argparse.ArgumentParser(description='Downloads the given user')
    parser.add_argument('-n', '--name', dest='name',
        help="The screen name of the user to download", required=True)
    parser.add_argument('-p', '--path', dest='path', required=False,
        default=DEFAULT_PATH, help='The path of the config file', type=str)

    args = parser.parse_args()

    download_user(args.name, args.path)
