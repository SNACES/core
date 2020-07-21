# TODO: implement lazy mode: tweets should have field that indicates processed or not
# lazy mode only returns tweets that have yet to be processed
class TweetMongoInputDAO:
    def __init__(self):
        self.global_tweets_collection = None
        self.user_tweets_collection = None
    
    def get_global_tweets(self, lazy=True):
        """
        Return unprocessed global tweets when lazy mode is toggled, 
        else return all global tweets in database.
        Format: [tweet text]
        """

        global_tweets = []

        if lazy:
            # TODO: not sure if we're querying for missing fields correctly
            global_tweet_doc_list = self.global_tweets_collection.find({
                'is_processed': {'$ne': True}
            })
        else:
            global_tweet_doc_list = self.global_tweets_collection.find()

        for global_tweet_doc in global_tweet_doc_list:
            tweet_text = global_tweet_doc['text']
            global_tweets.append(tweet_text)

        return tweet_text

    def get_user_tweets(self, lazy=True):
        """
        Return unprocessed user tweets when lazy mode is toggled, 
        else return all user tweets in database.
        Format: {user: [tweet text]}
        """
        
        user_to_tweets = {}

        if lazy:
            # user_tweet_doc_list = self.user_tweets_collection.find({
            #     '$or': [{'tweets.is_processed': False}, 
            #             {'tweets.is_processed': {"$exists": False}}
            #     ]          
            # })
            user_tweet_doc_list = self.user_tweets_collection.find({'tweets.is_processed': False})
        else:
            user_tweet_doc_list = self.user_tweets_collection.find()

        for user_doc in user_tweet_doc_list:
            user = user_doc['user']
            user_tweet_wrapper_list = user_doc['tweets']
            tweet_text = [tweet_wrapper['text'] for tweet_wrapper in user_tweet_wrapper_list]

            user_to_tweets[user] = tweet_text

        print(user_to_tweets)
        return user_to_tweets