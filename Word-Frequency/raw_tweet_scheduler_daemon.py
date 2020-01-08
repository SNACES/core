import sys
sys.path.append('../Twitter-Download')

import schedule
import time
import datetime
import daemon
from twitterDownloader import TwitterTweetDownloader
import os
from argparse import ArgumentParser

parser = ArgumentParser(description="")
parser.add_argument('--num-tweets-to-download', 
                    type=int,
                    help="Number of tweets to download daily",
                    required=True)

parser.add_argument('--time-to-download', 
                    type=str,
                    help="Time during the day to download tweets",
                    required=True)

parser.add_argument('--ds_location', 
                    type=str,
                    help="Location for the datastore to download to",
                    required=True)

parser.add_argument('--ds_name', 
                    type=str,
                    help="Name of the datastore",
                    required=True)

                     
args = parser.parse_args()

num_tweets_to_download = args.num_tweets_to_download
time_to_download = args.time_to_download
ds_location = args.ds_location
ds_name = args.ds_name

def download_daily_tweets():
    # num_tweets_to_download specified by config

    ds_config_path = os.getcwd() + "/../General/ds-init-config.yaml"
    twitterDownloader = TwitterTweetDownloader(ds_config_path)

    # tweets downloaded from a given date are organized into the same collection, identified by the date
    # when they are downloaded
    date = datetime.date.today().strftime("%Y-%m-%d")
    output_collection_name = "({})-RawTweets".format(date) 
    twitterDownloader.get_random_tweets(num_tweets_to_download, output_collection_name, ds_location, ds_name)

def run_scheduler():   
    # time to download specified by config

    schedule.every().day.at(time_to_download).do(download_daily_tweets)

    while True:
        schedule.run_pending()
        time.sleep(1)

with daemon.DaemonContext():
    run_scheduler()

# python3 raw_tweet_scheduler_daemon.py --num_tweets_to_download <num_tweets> --time_to_download <time> 