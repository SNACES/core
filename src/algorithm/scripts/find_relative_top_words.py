from src.algorithm.Activity.top_words_activity import TopWordsActivity
import argparse
import time
from src.algorithm.top_words.parser.parse_config import parse_from_file
from src.shared.utils import get_project_root

DEFAULT_PATH = str(get_project_root()) + "/src/algorithm/top_words/config/top_words.yaml"
DEFAULT_METHOD = "Label Propagation"

def top_words(cluster_num: int, base_user: str, cluster_type: str, path=DEFAULT_PATH):
    config = parse_from_file(path)

    activity = TopWordsActivity(config)
    activity.find_top_words(cluster_num, base_user,cluster_type)

if __name__ == "__main__":
    """
    Clean inactive users in the friends list.
    """
    parser = argparse.ArgumentParser(description='Get rid of inactive users')
    parser.add_argument('-c', '--cluster number', dest='cluster_num', required=True,
        help='which cluster to find top words', type=int)
    parser.add_argument('-u', '--user', dest='base_user', required=True,
        help='The target user', type=str)
    parser.add_argument('-t', '--clustering type', dest='cluster_type', required=False,
        default=DEFAULT_METHOD, help='Label Propagation / Max Modularity', type=str)
    parser.add_argument('-p', '--path', dest='path', required=False,
        default=DEFAULT_PATH, help='The path of the config file', type=str)

    args = parser.parse_args()

    top_words(args.cluster_num, args.base_user, args.cluster_type,args.path)