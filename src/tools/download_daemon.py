import schedule
import daemon
import time

from src.shared.utils import get_project_root
from src.process.download.twitter_downloader import TwitterTweetDownloader
from src.process.download.download_config_parser import DownloadConfigParser

def download_random_tweet():
    def main():
        tweet_downloader = TwitterTweetDownloader()
        config_path = get_project_root() / 'src' / 'process' / 'download' / 'download_config.yaml'
        download_config_parser = DownloadConfigParser(config_path)
        tweepy_getter, _ = download_config_parser.create_getter_DAOs()
        tweet_mongo_setter, _, _ = download_config_parser.create_setter_DAOs()
        tweet_downloader.gen_random_tweet(tweepy_getter, tweet_mongo_setter)

    with daemon.DaemonContext(chroot_directory=None, working_directory='./'):
        # schedule every second, rather than every day
        schedule.every().second.do(main)

        while True:
            schedule.run_pending()
            time.sleep(1)