from typing import Dict
from src.dao.twitter.twitter_dao import TwitterGetter
from src.dao.twitter.tweepy_twitter_dao import TweepyTwitterGetter

class TwitterDAOFactory():
    def create_getter(download_source: Dict) -> TwitterGetter:
        twitter_getter = None
        if download_source["type"] == "Tweepy":
            twitter_getter = TweepyTwitterGetter()
        else:
            raise Exception("Datastore type not supported")

        return twitter_getter
