import argparse
from src.shared.utils import get_project_root
from src.scripts.parser.parse_config import parse_from_file
from src.activity.rank_cluster_activity import RankClusterActivity

DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/rank_cluster_config.yaml"


def rank_cluster(seed_id: str, params=None, path=DEFAULT_PATH):
    config = parse_from_file(path)

    activity = RankClusterActivity(config)
    activity.rank_cluster(seed_id, params)


if __name__ == "__main__":
    """
    Short script to perform clustering on a social graph
    """
    parser = argparse.ArgumentParser(description='Downloads the given number of tweets')
    parser.add_argument('-s', '--seed_id', dest='seed_id', required=True,
        help='The seed id of the local neighbourhood to convert into a social graph', type=str)
    parser.add_argument('-p', '--path', dest='path', required=False,
        default=DEFAULT_PATH, help='The path of the config file', type=str)

    args = parser.parse_args()

    rank_cluster(args.seed_id, path=args.path)
