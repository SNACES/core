from functools import reduce

class TweetMongoOutputDAO:
    def __init__(self):
        super().__init__()
        self.global_processed_tweets_collection = None
        self.global_tweets_collection = None
        self.user_processed_tweets_collection = None
        self.user_tweets_collection = None
    
    def store_global_processed_tweets(self, processed_global_tweet_list):
        """
        Store global processed tweets into database.
        Format: {'tweet_words': [str]}
        """
        
        # Store
        for tweet_words in processed_global_tweet_list:
            self.global_processed_tweets_collection.insert_one({
                'tweet_words': tweet_words,
            })

    def store_user_processed_tweets(self, user_to_processed_tweet_list):
        """
        Store user processed tweets into database.
        Format: {'user': str, 'processed_tweets' [{'tweet_words': [str]}]}
        """
        
        # Store
        for user in user_to_processed_tweet_list:
            tweet_list = user_to_processed_tweet_list[user]
            processed_tweet_list = list(reduce(lambda a: {'tweet_words': a}, tweet_list))

            self.user_processed_tweets_collection.insert_one({
                'user': user,
                'processed_tweets': processed_tweet_list
            })

    def update_global_tweet_state(self):
        """
        Assume that all tweets in the global raw tweets collection have been processed and stored.
        Update processed field in global raw tweet docs to reflect this.
        """

        for global_tweet_doc in self.global_tweets_collection.find():
            id = global_tweet_doc['_id']
            global_tweet_doc['is_processed'] = True
            self.global_tweets_collection.update_one({'_id': id}, global_tweet_doc)

    def update_user_tweet_state(self):
        """
        Assume that all tweets in the user raw tweets collection have been processed and stored.
        Update processed field in user raw tweet docs to reflect this.
        """

        for user_doc in self.user_tweets_collection.find():
            user = user_doc['user']
            tweet_list = user_doc['tweets']

            for tweet in tweet_list:
                tweet['is_processed'] = True

            self.user_tweets_collection.update_one({'user': user}, user_doc)
