from src.activity.download_raw_tweets_activity import DownloadTweetsActivity
import argparse
import time
from src.scripts.parser.parse_config import parse_from_file
from src.shared.utils import get_project_root

DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/download_tweets_config.yaml"

def download_tweets(num: int, path=DEFAULT_PATH):
    config = parse_from_file(path)

    activity = DownloadTweetsActivity(config)
    activity.stream_random_tweets(num_tweets=num)

if __name__ == "__main__":
    """
    Short script to download tweets
    """
    parser = argparse.ArgumentParser(description='Downloads the given number of tweets')
    parser.add_argument('-n', '--num', dest='num', required=True,
        help='The number of tweets to download', type=int)
    parser.add_argument('-p', '--path', dest='path', required=False,
        default=DEFAULT_PATH, help='The path of the config file', type=str)

    args = parser.parse_args()

    download_tweets(args.num, args.path)
