import schedule
import daemon
import time

from src.shared.utils import get_project_root
from src.process.raw_tweet_processing.raw_tweet_processor import RawTweetProcessor
from src.process.raw_tweet_processing.rt_processing_config_parser import RawTweetProcessingConfigParser

def process_raw_tweet():
    def main():
        raw_processor = RawTweetProcessor()
        config_path = get_project_root() / 'src' / 'process' / 'raw_tweet_processing' / 'rt_processing_config.yaml'
        raw_process_parser = RawTweetProcessingConfigParser(config_path)
        tweet_getter = raw_process_parser.create_getter_DAOs()
        tweet_setter, processed_tweet_setter = raw_process_parser.create_setter_DAOs()
        raw_processor.gen_processed_global_tweets(tweet_getter, tweet_setter, processed_tweet_setter)

    with daemon.DaemonContext(chroot_directory=None, working_directory='./'):
        # schedule every second, rather than every day
        schedule.every().day.do(main)

        while True:
            schedule.run_pending()
            time.sleep(1)
