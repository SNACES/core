from src.activity.download_user_tweets_activity import DownloadUserTweetsActivity
import argparse
import time
from src.scripts.parser.parse_config import parse_from_file
from src.shared.utils import get_project_root

DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/download_user_tweets_config.yaml"

def download_user_tweets(name: str, path=DEFAULT_PATH):
    config = parse_from_file(path)

    activity = DownloadUserTweetsActivity(config)
    activity.download_user_tweets_by_screen_name(args.name)

if __name__ == "__main__":
    """
    Short script to download users
    """
    parser = argparse.ArgumentParser(description='Downloads the tweets for a given user')
    parser.add_argument('-n', '--screen_name', dest='name',
        help="The screen name of the user to download", required=True)
    parser.add_argument('-p', '--path', dest='path', required=False,
        default=DEFAULT_PATH, help='The path of the config file', type=str)

    args = parser.parse_args()

    download_user_tweets(args.name, args.path)
