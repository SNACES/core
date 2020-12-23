from src.activity.download_local_neighbourhood_tweets_activity import DownloadLocalNeighbourhoodTweetsActivity
import argparse
import time
from src.scripts.parser.parse_config import parse_from_file
from src.shared.utils import get_project_root

DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/download_local_neighbourhood_tweets_config.yaml"


def download_local_neighbourhood_tweets(name: str, path=DEFAULT_PATH):
    config = parse_from_file(path)

    activity = DownloadLocalNeighbourhoodTweetsActivity(config)
    activity.download_local_neighbourhood_tweets_by_user_id(name)


if __name__ == "__main__":
    """
    Short script to download tweets
    """
    parser = argparse.ArgumentParser(description='Downloads the tweets of all the users in a local neighbourhood of the given user')
    parser.add_argument('-n', '--name', dest='name', required=True,
        help='The name of the user to start on', type=str)
    parser.add_argument('-p', '--path', dest='path', required=False,
        default=DEFAULT_PATH, help='The path of the config file', type=str)

    args = parser.parse_args()

    download_local_neighbourhood_tweets(args.name, args.path)
