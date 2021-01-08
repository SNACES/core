from src.activity.process_local_neighbourhood_tweets_activity import ProcessLocalNeighbourhoodTweetsActivity
import argparse
import time
from src.scripts.parser.parse_config import parse_from_file
from src.shared.utils import get_project_root

DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/process_local_neighbourhood_tweets_config.yaml"


def process_local_neighbourhood_tweets(id: str, path=DEFAULT_PATH):
    config = parse_from_file(path)

    activity = ProcessLocalNeighbourhoodTweetsActivity(config)
    activity.process_local_neighbourhood_tweets(id)


if __name__ == "__main__":
    """
    Short script to process the tweets of a Local Neighbourhood
    """
    parser = argparse.ArgumentParser(description='Processes the tweets of all the users in a local neighbourhood of the given user')
    parser.add_argument('-i', '--id', dest='id', required=True,
        help='The seed id of the local neighbourhood', type=str)
    parser.add_argument('-p', '--path', dest='path', required=False,
        default=DEFAULT_PATH, help='The path of the config file', type=str)

    args = parser.parse_args()

    process_local_neighbourhood_tweets(args.id, args.path)
