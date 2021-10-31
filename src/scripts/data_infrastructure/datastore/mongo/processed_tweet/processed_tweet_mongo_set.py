from src.shared.utils import get_unique_list

class ProcessedTweetMongoSetDAO:
    """
    A class that stores processed tweet data collection from MongoDB.

    @private 
        global_processed_tweet_collection: list of global processed tweet data
        user_processed_tweet_collection: list of processed tweet collection for each users
    """
    def __init__(self):
        """
        Initialize a new ProcessedTweetMongoSetDAO class.
        """
        self.global_processed_tweet_collection = None
        self.user_processed_tweet_collection = None
    
    def store_global_processed_tweets(self, processed_global_tweet_list):
        """
        Store global processed tweets into the database.
        Format: {'tweet_words': [str]}

        @param processed_global_tweet_list: list of processed global tweet to be stored
        """
        
        for tweet_words in processed_global_tweet_list:
            if tweet_words:
                self.global_processed_tweet_collection.insert_one({
                    'tweet_words': tweet_words,
                })

    def store_user_processed_tweets(self, user_to_processed_tweet_list):
        """
        Store user processed tweets into database.
        Format: {'user': str, 'processed_tweets' [{'tweet_words': [str]}]}

        @param user_to_processed_tweet_list: list of processed tweet of each user to be stored
        """
        
        for user in user_to_processed_tweet_list:
            tweet_list = user_to_processed_tweet_list[user]
            processed_tweet_list = list(map(lambda a: {'tweet_words': a}, tweet_list))

            user_doc = self.user_processed_tweet_collection.find_one({
                'user': user
            })
            if user_doc:
                # Update
                user_doc['processed_tweets'] += processed_tweet_list
                self.user_processed_tweet_collection.replace_one({
                    'user': user
                }, user_doc)
            else:
                # Add new entry
                self.user_processed_tweet_collection.insert_one({
                    'user': user,
                    'processed_tweets': processed_tweet_list
                })

    def update_global_processed_tweet_state(self):
        """
        Assume that all tweets in the global processed tweets collection 
        have their words counted and word count vectors stored.
        Update is_counted field in global processed tweet docs to reflect this.
        """

        for global_tweet_doc in self.global_processed_tweet_collection.find():
            id = global_tweet_doc['_id']
            global_tweet_doc['is_counted'] = True
            self.global_processed_tweet_collection.replace_one({'_id': id}, global_tweet_doc)

    def update_user_processed_tweet_state(self):
        """
        Assume that all tweets in the user processed tweets collection 
        have their words counted and word count vectors stored.
        Update is_counted field in user processed tweet docs to reflect this.
        """

        for user_doc in self.user_processed_tweet_collection.find():
            user = user_doc['user']
            processed_tweet_list = user_doc['processed_tweets']

            for tweet in processed_tweet_list:
                tweet['is_counted'] = True

            self.user_processed_tweet_collection.replace_one({'user': user}, user_doc)
