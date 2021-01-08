from src.algorithm.Activity.count_connect_activity import CountConnectActivity
import argparse
import time
from src.algorithm.count_connect.parser.parse_config import parse_from_file
from src.shared.utils import get_project_root

DEFAULT_PATH = str(get_project_root()) + "/src/algorithm/count_connect/config/count_connect.yaml"
DEFAULT_METHOD = "Label Propagation"

def count_connected(cluster_num_1: int, cluster_num_2: int, base_user: str, cluster_type: str, path=DEFAULT_PATH):
    config = parse_from_file(path)

    activity = CountConnectActivity(config)
    activity.count_connect_between_cluster(cluster_num_1, cluster_num_2, base_user,cluster_type)

if __name__ == "__main__":
    """
    Clean inactive users in the friends list.
    """
    parser = argparse.ArgumentParser(description='count connectedness between clusters')
    parser.add_argument('-c1', '--first cluster number', dest='cluster_num_1', required=True,
        help='the first cluster to compare', type=int)
    parser.add_argument('-c2', '--second cluster number', dest='cluster_num_2', required=True,
        help='the second cluster to compare', type=int)
    parser.add_argument('-u', '--user', dest='base_user', required=True,
        help='The target user', type=str)
    parser.add_argument('-t', '--clustering type', dest='cluster_type', required=False,
        default=DEFAULT_METHOD, help='Label Propagation / Max Modularity', type=str)
    parser.add_argument('-p', '--path', dest='path', required=False,
        default=DEFAULT_PATH, help='The path of the config file', type=str)

    args = parser.parse_args()

    count_connected(args.cluster_num_1, args.cluster_num_2, args.base_user, args.cluster_type,args.path)