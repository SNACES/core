from src.activity.download_raw_tweets_activity import DownloadUserTweetsActivity
import schedule
import daemon
import time

"""
Note, daemon library only works for UNIX
"""

if __name__ == "__main__":
    """
    Short script to download tweets
    """
    config = {
        "location": "mongodb://localhost:27017",
        "datastore-name": "RawTweetStore",
        "collection-name": "RawTweets"
    }

    activity = DownloadUserTweetsActivity(config)

    with daemon.DaemonContext(chroot_directory=None, working_directory="./"):
        # schedule every second
        schedule.every().second.do(activity.download_random_tweet)

        while True:
            schedule.run_pending()
            time.sleep(1)
