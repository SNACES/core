from src.shared.utils import get_unique_list

class TweetMongoSetDAO():
    """
    A class that stores tweet data collection from MongoDB.

    @private 
        global__tweet_collection: list of global processed tweet data
        user_tweet_collection: list of processed tweet collection for each users
    """
    def __init__(self):
        """
        Initialize a new TweetMongoSetDAO class.
        """
        self.global_tweet_collection = None
        self.user_tweet_collection = None

    def store_tweet_by_user(self, user, tweets, retweets):
        """
        Store user processed tweets into the database.

        @param user: specific users
        @param tweets: tweets of the users
        @param retweets: retweets of the users
        """
        user_doc = self.user_tweet_collection.find_one({
            'user': user
        })

        if user_doc:
            # Update 
            user_doc['tweets'] += tweets
            user_doc['tweets'] = self._get_unique_tweet_list(user_doc['tweets'])
            user_doc['retweets'] += retweets
            user_doc['retweets'] = self._get_unique_tweet_list(user_doc['retweets'])
            self.user_tweet_collection.replace_one({
                'user': user
            }, user_doc)
        else:
            # Add new entry
            self.user_tweet_collection.insert_one({
                'user': user,
                'tweets': tweets,
                'retweets': retweets
            }) 

    def store_random_tweet(self, tweet):
        """
        Store global random tweets.

        @param tweet: a list of global random tweets
        """
        if tweet:
            self.global_tweet_collection.insert_one({
                'text': tweet['text']
            }) 

    def _get_unique_tweet_list(self, tweet_list):
        # Assume that tweet_list is organized like so: 
        # A = {raw tweets that have been processed} 
        # B = {tweets that have not been processed}
        # [A, B]
        tweet_id_to_tweet_obj = {}
        for tweet in tweet_list:
            tweet_id = tweet['id']
            if tweet_id not in tweet_id_to_tweet_obj: 
                tweet_id_to_tweet_obj[tweet_id] = tweet

        unique_tweet_list = [tweet_id_to_tweet_obj[tweet_id] 
                             for tweet_id in tweet_id_to_tweet_obj]
             
        return unique_tweet_list

    def update_global_tweet_state(self):
        """
        Assume that all tweets in the global raw tweets collection have been processed and stored.
        Update processed field in global raw tweet docs to reflect this.
        """

        for global_tweet_doc in self.global_tweet_collection.find():
            id = global_tweet_doc['_id']
            global_tweet_doc['is_processed'] = True
            self.global_tweet_collection.replace_one({'_id': id}, global_tweet_doc)

    def update_user_tweet_state(self):
        """
        Assume that all tweets in the user raw tweets collection have been processed and stored.
        Update processed field in user raw tweet docs to reflect this.
        """

        for user_doc in self.user_tweet_collection.find():
            user = user_doc['user']
            tweet_list = user_doc['tweets']

            for tweet in tweet_list:
                tweet['is_processed'] = True

            self.user_tweet_collection.replace_one({'user': user}, user_doc)


