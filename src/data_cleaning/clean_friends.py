from src.data_cleaning.Activity.clean_friends_activity import FriendsCleaningActivity
import argparse
import time
from src.data_cleaning.parser.parse_config import parse_from_file
from src.shared.utils import get_project_root

DEFAULT_PATH = str(get_project_root()) + "/src/data_cleaning/config/friends_cleaning.yaml"

def friends_cleaning(threshold: int, method: str, base_user: str, path=DEFAULT_PATH):
    config = parse_from_file(path)

    activity = FriendsCleaningActivity(config)
    if method == "1":
        activity.clean_by_friends(base_user, threshold)
    elif method == "2":
        activity.clean_by_tweets(base_user, threshold)
    else:
        raise NotImplementedError()

if __name__ == "__main__":
    """
    Clean inactive users in the friends list.
    """
    parser = argparse.ArgumentParser(description='Get rid of inactive users')
    parser.add_argument('-t', '--threshold', dest='threshold', required=True,
        help='The threshold of data cleaning', type=int)
    parser.add_argument('-u', '--user', dest='base_user', required=True,
        help='The target user', type=str)
    parser.add_argument('-m', '--method', dest='method', required=True,
        help='1 is cleaning by friends number, 2 is cleaning by tweets number', type=str)
    parser.add_argument('-p', '--path', dest='path', required=False,
        default=DEFAULT_PATH, help='The path of the config file', type=str)

    args = parser.parse_args()

    friends_cleaning(args.threshold, args.method, args.base_user, args.path)