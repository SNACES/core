import argparse
from src.shared.utils import get_project_root
from src.scripts.parser.parse_config import parse_from_file
from src.activity.process_tweet_activity import ProcessTweetActivity

DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/process_tweet_config.yaml"


def process_tweet(id: str, path=DEFAULT_PATH):
    config = parse_from_file(path)

    activity = ProcessTweetActivity(config)
    activity.process_tweet_by_id(id)


if __name__ == "__main__":
    """
    Short script to process tweets
    """
    parser = argparse.ArgumentParser(description='Processes the given tweet')
    parser.add_argument('-i', '--id', dest='id',
        help="The id of the tweet to process", required=True, type=str)
    parser.add_argument('-p', '--path', dest='path', required=False,
        default=DEFAULT_PATH, help='The path of the config file', type=str)

    args = parser.parse_args()

    process_tweet(args.id, args.path)
