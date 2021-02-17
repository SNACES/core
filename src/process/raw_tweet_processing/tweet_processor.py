from src.model.tweet import Tweet
from src.model.processed_tweet import ProcessedTweet
from src.model.local_neighbourhood import LocalNeighbourhood
from src.dao.raw_tweet.getter.raw_tweet_getter import RawTweetGetter
from src.dao.processed_tweet.setter.processed_tweet_setter import ProcessedTweetSetter
from src.shared.logger_factory import LoggerFactory

log = LoggerFactory.logger(__name__)

class TweetProcessor():
    def __init__(self, raw_tweet_getter: RawTweetGetter, processed_tweet_setter: ProcessedTweetSetter):
        self.raw_tweet_getter = raw_tweet_getter
        self.processed_tweet_setter = processed_tweet_setter

    def process_tweet_by_id(self, id: str):
        tweet = self.raw_tweet_getter.get_tweet_by_id(id)
        processed_tweet = ProcessedTweet.fromTweet(tweet)
        self.processed_tweet_setter.store_processed_tweet(processed_tweet)

    def process_tweets_by_user_id(self, user_id: str):
        tweets = self.raw_tweet_getter.get_tweets_by_user_id(user_id)
        if tweets is not None:
            ids = self.processed_tweet_setter.get_ids_by_user(user_id)
            for tweet in tweets:
                if tweet.id not in ids:
                    processed_tweet = ProcessedTweet.fromTweet(tweet)
                    self.processed_tweet_setter.store_processed_tweet(processed_tweet, check=False)
            log.info("Processed " + str(len(tweets)) + " Tweets for " + str(user_id))

    def process_tweets_by_local_neighbourhood(self, local_neighbourhood: LocalNeighbourhood):
        user_ids = local_neighbourhood.get_user_id_list()
        num_ids = len(user_ids)
        for i in range(num_ids):
            user_id = user_ids[i]
            self.process_tweets_by_user_id(user_id)
            log.log_progress(log, i, num_ids)
