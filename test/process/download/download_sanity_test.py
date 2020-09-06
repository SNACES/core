import datetime

from src.shared.utils import get_project_root
from src.process.download.twitter_downloader import TwitterTweetDownloader, TwitterFriendsDownloader, TwitterFollowersDownloader
from src.process.download.download_config_parser import DownloadConfigParser

twitter_downloader = TwitterTweetDownloader()
friends_downloader = TwitterFriendsDownloader()
followers_downloader = TwitterFollowersDownloader()

# Init query variables
id = "animesh_garg"
start_date = datetime.datetime(2019, 6, 1, 0, 0, 0)
end_date = datetime.datetime(2020, 7, 17, 0, 0, 0)

# Init input and output daos
config_path = get_project_root() / 'src' / 'process' / 'download' / 'download_config.yaml'
download_config_parser = DownloadConfigParser(config_path)
tweepy_get = download_config_parser.create_getter_DAOs()
tweet_mongo_set, user_friends_set, user_followers_set = download_config_parser.create_setter_DAOs()

# Test methods
# twitter_downloader.gen_user_tweets(id, tweepy_get, tweet_mongo_set, 20)
# twitter_downloader.gen_user_tweets(id, tweepy_get, tweet_mongo_set, 50, start_date, end_date)
# twitter_downloader.gen_random_tweet(tweepy_get, tweet_mongo_set)
# friends_downloader.gen_friends_by_screen_name(id, tweepy_get, user_friends_set, 10)
# followers_downloader.gen_followers_by_screen_name(id, tweepy_get, user_followers_set, 10)

