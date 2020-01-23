import sys
sys.path.append('../Twitter-Download')

import schedule
import time
import datetime
import daemon
from twitterDownloader import TwitterTweetDownloader
import os
from argparse import ArgumentParser
from word_frequency import WordFrequency
import yaml

parser = ArgumentParser(description="")
parser.add_argument('--config-file-name', 
                    type=str,
                    help="Name for configruation file",
                    required=True)
                     
args = parser.parse_args()
config_file_name = args.config_file_name
wf_config_path = os.getcwd() + "/" + config_file_name
ds_config_path = os.getcwd() + "/../General/ds-init-config.yaml" # TODO:

def download_raw_tweets(ds_config_path, output_collection_name, download_ds_config):
    twitter_downloader = TwitterTweetDownloader(ds_config_path)

    tweet_doc = twitter_downloader.get_random_tweet(output_collection_name, download_ds_config)
    num_tweets_downloaded = 1 if tweet_doc != None else 0

    # log to text file
    file1 = open("log.txt","a")
    file1.write(str(num_tweets_downloaded) + ' Tweets downloaded \n')
    file1.close() 

    return tweet_doc

def parse_download_ds_config(collection_name):
    return parse_config(collection_name, 'download-datastore')

def parse_processed_ds_config(collection_name):
    return parse_config(collection_name, 'processed-datastore')

def parse_config(collection_name, config_type):
    with open(wf_config_path, 'r') as stream:
        try:
            parsed_config = yaml.safe_load(stream)
            result = parsed_config[config_type]
            result['collection-name'] = collection_name
            
            return result
        except yaml.YAMLError as exc:
            print(exc)

def main():
    # tweets from a given date are organized into the same collection, identified by the date
    # when they are downloaded
    date = datetime.date.today().strftime("%Y-%m-%d")
    raw_tweet_collection_name = "({})-RawTweets".format(date) 

    download_ds_config = parse_download_ds_config(raw_tweet_collection_name)
    tweet_doc = download_raw_tweets(ds_config_path, raw_tweet_collection_name, download_ds_config)
    
    if tweet_doc != None:
        word_frequency = WordFrequency(ds_config_path)
        processed_ds_collection_name = "({})-ProcessedTweets".format(date)
        processed_ds_config = parse_processed_ds_config(processed_ds_collection_name)
        word_frequency.process_raw_tweets(tweet_doc, processed_ds_collection_name, processed_ds_config)

def run_scheduler():   
    # schedule every second, rather than every day
    schedule.every().second.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)

# with daemon.DaemonContext(chroot_directory=None, working_directory='./'):
#     run_scheduler()

run_scheduler()
    

# TODO: need to handle case when can't connect to Mongo >> raise exception

# python3 word_frequency_scheduler_daemon.py --config-file-name word-freq-ds-config.yaml