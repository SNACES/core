import argparse
import time
from src.scripts.parser.parse_config import parse_from_file
from src.shared.utils import get_project_root

from src.shared.logger_factory import LoggerFactory
from src.dependencies.injector import Injector
from src.shared.utils import get_project_root

log = LoggerFactory.logger(__name__)

DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/default_config.yaml"


def check_following(user_name: str, path=DEFAULT_PATH):

    injector = Injector.get_injector_from_file(path)
    process_module = injector.get_process_module()
    dao_module = injector.get_dao_module()

    user_friend_getter = dao_module.get_user_friend_getter()
    friends_cleaner = process_module.get_extended_friends_cleaner()
    user_getter = dao_module.get_user_getter()
    ranking_getter = dao_module.get_ranking_getter()

    seed_id = user_getter.get_user_by_screen_name(user_name).id

    news = ['nytimes', 'kylegriffin1', 'propublica', 'TheAtlantic', 'brianstelter',
            'NewYorker']

    ml = ['mer__edith', 'timnitGebru', 'merbroussard', 'rajiinio']

    for name in ml:
        log.info(name)
        user = user_getter.get_user_by_screen_name(name)
        friends = user_friend_getter.get_user_friends_ids(str(user.id))
        local_friends = []
        for name2 in ml:
            user2 = user_getter.get_user_by_screen_name(name2)
            if user2.id in friends:
                local_friends.append(name2)
        log.info(local_friends)

    # for name in news:
    #     log.info(name)
    #     user = user_getter.get_user_by_screen_name(name)
    #     friends = user_friend_getter.get_user_friends_ids(str(user.id))
    #     local_friends = []
    #     for name2 in ml:
    #         user2 = user_getter.get_user_by_screen_name(name2)
    #         if user2.id in friends:
    #             local_friends.append(name2)
    #     log.info(local_friends)


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

    check_following(args.name, args.path)
