# lazy mode: tweets should have field that indicates processed or not
# lazy mode only returns tweets that have yet to be processed
class TweetMongoGetDAO:
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
            global_tweet_doc_list = self.global_tweets_collection.find({
                'is_processed': {'$ne': True}
            })
        else:
            global_tweet_doc_list = self.global_tweets_collection.find()

        for global_tweet_doc in global_tweet_doc_list:
            tweet_text = global_tweet_doc['text']
            global_tweets.append(tweet_text)

        return global_tweets

    def get_user_tweets(self, get_retweets=False, lazy=True):
        """
        Return unprocessed user tweets when lazy mode is toggled, 
        else return all user tweets in database. Get retweets if get_tweets is toggled.
        Format: {user: [tweet text]}
        """
        
        user_to_tweets = {}
        query_type = 'retweets' if get_retweets else 'tweets'
        if lazy:
            pipeline = ([{
                '$project': {
                    'user': True,
                    query_type: {
                        '$filter': {
                        'input': "$tweets",
                        'as': "t",
                        'cond': {'$ne': ['$$t.is_processed', True]}}
                        }
                    }
                }
            ])
            user_tweet_doc_list = self.user_tweets_collection.aggregate(pipeline)
        else:
            user_tweet_doc_list = self.user_tweets_collection.find()

        for user_doc in user_tweet_doc_list:
            user = user_doc['user']
            user_tweet_wrapper_list = user_doc[query_type] 
            tweet_text = [tweet_wrapper['text'] for tweet_wrapper in user_tweet_wrapper_list]

            user_to_tweets[user] = tweet_text

        return user_to_tweets

    # TODO:
    def get_tweets_by_user_in_timeframe(self, user, start_date, end_date, get_retweets=False):
        pass
    
    # TODO:
    def get_tweets_by_user(self, user, get_retweets=False):
        pass
    
