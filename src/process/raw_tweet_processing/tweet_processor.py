from src.model.tweet import Tweet
from src.model.processed_tweet import ProcessedTweet
from src.model.local_neighbourhood import LocalNeighbourhood
from src.dao.raw_tweet.getter.raw_tweet_getter import RawTweetGetter
from src.dao.processed_tweet.setter.processed_tweet_setter import ProcessedTweetSetter
from src.shared.utils import print_progress


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
            for tweet in tweets:
                if not self.processed_tweet_setter.contains_tweet(tweet):
                    processed_tweet = ProcessedTweet.fromTweet(tweet)
                    self.processed_tweet_setter.store_processed_tweet(processed_tweet)

    def process_tweets_by_local_neighbourhood(self, local_neighbourhood: LocalNeighbourhood):
        print("Starting")

        user_ids = local_neighbourhood.get_user_id_list()
        num_ids = len(user_ids)
        for i in range(num_ids):
            user_id = user_ids[i]
            self.process_tweets_by_user_id(user_id)
            print_progress(i, num_ids)

        print("Done")
