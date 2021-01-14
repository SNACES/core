import argparse
from src.shared.utils import get_project_root
from src.dependencies.injector import Injector

DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/download_user_config.yaml"


def download_user(name: str, path=DEFAULT_PATH):
    injector = Injector.get_injector_from_file(path)
    process_module = injector.get_process_module()

    user_downloader = process_module.get_user_downloader()

    user_downloader.download_user_by_screen_name(name)

if __name__ == "__main__":
    """
    Short script to download users
    """
    parser = argparse.ArgumentParser(description='Downloads the given user')
    parser.add_argument('-n', '--name', dest='name',
        help="The screen name of the user to download", required=True)
    parser.add_argument('-p', '--path', dest='path', required=False,
        default=DEFAULT_PATH, help='The path of the config file', type=str)

    args = parser.parse_args()

    download_user(args.name, args.path)
