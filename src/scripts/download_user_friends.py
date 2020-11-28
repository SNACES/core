from src.activity.download_user_friends_activity import DownloadUserFriendsActivity
import argparse
import time
from src.scripts.parser.parse_config import parse_from_file
from src.shared.utils import get_project_root

DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/download_user_friends_config.yaml"

def download_user_friends(name: str, saturated=False, path=DEFAULT_PATH):
    config = parse_from_file(path)

    activity = DownloadUserFriendsActivity(config)
    activity.download_friends_by_screen_name(name, saturated=saturated)

if __name__ == "__main__":
    """
    Short script to download users
    """
    parser = argparse.ArgumentParser(description='Downloads the given user')
    parser.add_argument('-n', '--screen_name', dest='name',
        help="The screen name of the user to download", required=True)
    parser.add_argument('-s', '--saturated', dest='saturated', required=False,
        action='store_true',
        help='If true, downloads full user objects, otherwise just downloads ids')
    parser.add_argument('-p', '--path', dest='path', required=False,
        default=DEFAULT_PATH, help='The path of the config file', type=str)

    args = parser.parse_args()

    download_user_friends(args.name, saturated=args.saturated, path=args.path)
