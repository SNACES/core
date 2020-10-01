class ProcessedTweetMongoGetDAO():
    """
    A class that gets processed tweet data collection from MongoDB.

    @private 
        global_processed_tweet_collection: list of global processed tweet data
        user_processed_tweet_collection: list of processed tweet collection for each users
    """
    def __init__(self):
        """
        Initialize a new ProcessedTweetMongoGetDAO class.
        """
        self.global_processed_tweet_collection = None
        self.user_processed_tweet_collection = None
    
    def get_global_tweet_words(self, lazy=True):
        """
        Generate a list of all words from tweets in the global processed tweets collection.
        Input database doc if of format: {'tweet_words': [str]}

        @param lazy: update the flag of data from uncounted to iscounted, if lazy is True
        @return: list of global tweet word count
        """

        global_tweet_words = []
        if lazy:
            processed_tweet_list = self.global_processed_tweet_collection.find({
                'is_counted': {'$ne': True}
            })
        else:
            processed_tweet_list = self.global_processed_tweet_collection.find()

        # Run through tweets in collection and collect words from tweets
        for tweet_doc in processed_tweet_list:
            global_tweet_words.extend(tweet_doc['tweet_words'])

        return global_tweet_words

    def get_user_tweet_words(self, lazy=True): 
        """
        Return for each user in a list of all words from tweets in the user processed tweets collection.
        Input database doc format: {'user': str, 'processed_tweets' [{'tweet_words': [str]}]}
        
        @lazy: update the flag of data from uncounted to iscounted, if lazy is True
        @return: list of global tweet word count for each user, with output format: {user: [words]}
        """

        user_to_tweet_words = {}

        if lazy:
            pipeline = ([{
                '$project': {
                    'user': True,
                    'processed_tweets': {
                        '$filter': {
                        'input': "$processed_tweets",
                        'as': "p",
                        'cond': {'$ne': ['$$p.is_counted', True]}}
                        }
                    }
                }
            ])
            user_tweet_doc_list = self.user_processed_tweet_collection.aggregate(pipeline)
        else:
            user_tweet_doc_list = self.user_processed_tweet_collection.find()

        # Run through tweets in collection and collect words from tweets
        for user_doc in user_tweet_doc_list:
            user = user_doc['user']
            tweet_words = []
            
            for processed_tweet in user_doc['processed_tweets']:
                tweet_words.extend(processed_tweet['tweet_words'])

            user_to_tweet_words[user] = tweet_words

        return user_to_tweet_words