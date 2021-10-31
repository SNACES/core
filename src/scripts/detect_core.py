import argparse
from src.dependencies.injector import Injector
from src.shared.utils import get_project_root
from src.shared.logger_factory import LoggerFactory

log = LoggerFactory.logger(__name__)

DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/detect_core_config.yaml"


def detect_core(name: int, path=DEFAULT_PATH):
    """Runs the core detection.
    """
    try:
        # Construct an Injector with database info
        injector = Injector.get_injector_from_file(path)
        # Create a process module for Injector
        log.info("Creating Process Module...")
        process_module = injector.get_process_module()
        # Get core detector from process module
        log.info("Creating Core Detector...")
        core_detector = process_module.get_core_detector()
        # detect core by using the input twitter username
        log.info("Begins core detection:")
        core_detector.detect_core_by_screen_name(name)
    except Exception as e:
        log.exception(e)
        exit()


if __name__ == "__main__":
    """
    Short script to download tweets
    """
    parser = argparse.ArgumentParser(description='Downloads the given number of tweets')
    parser.add_argument('-n', '--name', dest='name', required=True,
        help='The name of the user to start on', type=str)
    parser.add_argument('-p', '--path', dest='path', required=False,
        default=DEFAULT_PATH, help='The path of the config file', type=str)
    args = parser.parse_args()
    detect_core(args.name, args.path)
