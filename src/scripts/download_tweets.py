from src.activity.download_raw_tweets_activity import DownloadTweetsActivity
import argparse
import time

if __name__ == "__main__":
    """
    Short script to download tweets
    """
    parser = argparse.ArgumentParser(description='Downloads the given number of tweets')
    parser.add_argument('-n',
        '--num', dest='num', required=True, help='The number of tweets to download', type=int)

    args = parser.parse_args()

    config = {
        "location": "mongodb://localhost:27017",
        "datastore-name": "Data",
        "collection-name": "RawTweets"
    }

    activity = DownloadTweetsActivity(config)
    activity.stream_random_tweets(num_tweets=args.num)
