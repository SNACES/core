#!/usr/bin/env python
import click    
from src.shared.utils import get_project_root

# Download
import datetime
import dateutil
import src.tools.download_daemon as download_daemon
from src.process.download.twitter_downloader import TwitterTweetDownloader, TwitterFriendsDownloader, TwitterFollowersDownloader
from src.process.download.download_config_parser import DownloadConfigParser

# TODO:
"""
1. ask for "process/app/experiment"
3. get args for process
2. (optional) ask for path
4. create appropriate config parsers based on experiment type 
5. run process
"""

# Event handlers
def run_download():
    print("Provide the full path the the download config(leave blank to set to default)")
    default_path = get_project_root() / 'src' / 'process' / 'download' / 'download_config.yaml'
    download_config_path = click.prompt("Path", default_path)
    download_config_parser = DownloadConfigParser(download_config_path)
    tweepy_getter, user_friends_getter = download_config_parser.create_getter_DAOs()
    tweet_mongo_setter, user_friends_setter, user_followers_setter = download_config_parser.create_setter_DAOs()

    print("Types of Download:")
    print("1. Twitter Tweet Download")
    print("2. Twitter Friends Download")
    print("3. Twitter Followers Download")
    download_type = click.prompt("Choose a download type")

    if int(download_type) == 1:
        tweet_downloader = TwitterTweetDownloader()
        print("Types of tweets:")
        print("1. User Tweets")
        print("2. Random Tweets")
        tweet_type = click.prompt("Choose what to download")
        if int(tweet_type) == 1:
            print("Downloading User Tweets")
            user = click.prompt("User")
            num_tweets = click.prompt("Number of Tweets(leave blank to get all)")
            if click.confirm("Do you want to specify a start and end date?"):
                start_date = dateutil.parser(click.prompt("Start Date(YYYY-MM-DD)"))
                end_date = dateutil.parser(click.prompt("End Date(YYYY-MM-DD)"))
                tweet_downloader.gen_user_tweets(user, tweepy_getter, tweet_mongo_setter, num_tweets, start_date, end_date)
            else:
                tweet_downloader.gen_user_tweets(user, tweepy_getter, tweet_mongo_setter, num_tweets)
        elif int(tweet_type) == 2:
            print("Downloading Random Tweets")
            print("Due to Tweepy constraints, if you want to download multiple tweets, you should launch a daemon")
            if click.confirm("Do you wish to launch a daemon to download random tweets?"):
                print("Launching daemon")
                download_daemon.download_random_tweet()
            else:    
                tweet_downloader.gen_random_tweet(tweepy_getter, tweet_mongo_setter)
    elif int(download_type) == 2:
        print("Downloading friends")
        user = click.prompt("User")
        num_friends = click.prompt("Number of Friends(leave blank to get all)")
        friends_downloader = TwitterFriendsDownloader()
        friends_downloader.gen_friends_by_screen_name(user, tweepy_getter, user_friends_setter, num_friends)
    elif int(download_type) == 3:
        print("Downloading followers")
        user = click.prompt("User")
        num_followers = click.prompt("Number of Followers(leave blank to get all)")
        followers_downloader = TwitterFollowersDownloader()
        followers_downloader.gen_followers_by_screen_name(user, tweepy_getter, user_followers_setter, num_followers)
    else:
        raise Exception("Invalid input")

def run_rt_processing():
    pass

def run_wf():
    pass

def run_social_graph():
    pass

def run_clustering():
    pass

@click.command()
def main():
    print("====================================================")
    print("                       SNACES                       ")
    print("Social Network Algorithm Contained Experiment System")
    print("====================================================")
    print("Processes:")
    print("1. Download")
    print("2. Raw Tweet Processing")
    print("3. Word Frequency")
    print("4. Social Graph")
    print("5. Clustering")
    # print("\n")

    val = click.prompt("Choose a process")
    if int(val) == 1:
        run_download()
    elif int(val) == 2:
        run_rt_processing()
    elif int(val) == 3:
        run_wf()
    elif int(val) == 4:
        run_social_graph()
    elif int(val) == 5:
        run_clustering()
    else:
        raise Exception("Invalid input")

if __name__ == "__main__":
    main()

