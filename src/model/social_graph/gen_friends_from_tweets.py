import src.dependencies.injector as sdi
from src.shared.logger_factory import LoggerFactory
from src.process.data_cleaning.data_cleaning_distributions import jaccard_similarity
from src.shared.utils import get_project_root
from src.model.local_neighbourhood import LocalNeighbourhood
# Just for type signatures
from typing import List
from src.model.user import User
from src.model.social_graph.social_graph import SocialGraph
from src.model.cluster import Cluster
import argparse

log = LoggerFactory.logger(__name__)
DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/create_social_graph_and_cluster_config.yaml"

def generate_friend_graph_from_tweets(screen_name: str, tweet_thresh: int, path=DEFAULT_PATH):
    try:
        log.info("Creating friend graph from tweets")
        injector = sdi.Injector.get_injector_from_file(path)
        process_module = injector.get_process_module()
        dao_module = injector.get_dao_module()

        tweet_getter = dao_module.get_user_tweet_getter()
        friend_setter = dao_module.get_user_friend_from_tweets_setter()
        user = get_user_by_screen_name(screen_name, path)

        retweets = tweet_getter.get_retweets_by_user_id(user)
        dic = {}
        # If number of retweets of tweets from retweet user is greater than threshold, add to friend set
        for retweet in retweets:
            if retweet.retweet_user_id in dic:
                dic[retweet.retweet_user_id] += 1
            else:
                dic[retweet.retweet_user_id] = 1
        
        friends = [k for k, v in dic.items() if v >= tweet_thresh]
        friend_setter.store_friends(user, friends)
    except Exception as e:
        log.exception(e)
        log.exception(f'{user.screen_name} {user.id} {type(user.id)}')
        exit()


def get_user_by_screen_name(screen_name: str, path=DEFAULT_PATH) -> User:
    """Returns a user object from their twitter screen name."""
    injector = sdi.Injector.get_injector_from_file(path)
    dao_module = injector.get_dao_module()
    user_getter = dao_module.get_user_getter()
    user = user_getter.get_user_by_screen_name(screen_name)
    return user

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create friends list from tweets')
    parser.add_argument('-n', '--name', dest='name', required=True,
        help='The name of the user to start on', type=str)

    args = parser.parse_args()

    generate_friend_graph_from_tweets(args.name, args.path)