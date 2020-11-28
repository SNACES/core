from src.activity.download_user_tweets_activity import DownloadUserTweetsActivity
import argparse
import time

if __name__ == "__main__":
    """
    Short script to download users
    """
    parser = argparse.ArgumentParser(description='Downloads the tweets for a given user')
    parser.add_argument('-n', '--screen_name', dest='name',
        help="The screen name of the user to download", required=True)

    args = parser.parse_args()

    config = {
        "location": "mongodb://localhost:27017",
        "datastore-name": "Data",
        "collection-name": "UserTweets"
    }

    activity = DownloadUserTweetsActivity(config)
    activity.download_user_tweets_by_screen_name(args.name)
