from src.shared.lib import get_unique_list

class DownloadMongoOutputDAO():
    def __init__(self):
        self.global_tweet_collection = None
        self.user_tweet_collection = None
        self.user_timeframe_tweet_collection = None
        self.user_friends_by_id_collection = None
        self.user_friends_by_name_collection = None
        self.user_following_by_id_collection = None
        self.user_following_by_name_collection = None

    def store_tweet_by_timeframe_user(self, user, start_date, end_date, tweets):
        user_doc = self.user_timeframe_tweet_collection.find_one({
            'user': user
        })

        if user_doc:
            # Update
            user_doc['tweets'] += tweets
            user_doc['tweets'] = self._get_unique_tweet_list(user_doc['tweets'])
            self.user_timeframe_tweet_collection.replace_one({
                'user': user
            }, user_doc)
        else:
            # Add new entry
            self.user_timeframe_tweet_collection.insert_one({
                'user': user,
                'start': start_date,
                'end': end_date,
                'tweets': tweets
            }) 

    def store_tweet_by_user(self, user, tweets):
        user_doc = self.user_tweet_collection.find_one({
            'user': user
        })

        if user_doc:
            # Update
            user_doc['tweets'] += tweets
            user_doc['tweets'] = self._get_unique_tweet_list(user_doc['tweets'])
            self.user_tweet_collection.replace_one({
                'user': user
            }, user_doc)
        else:
            # Add new entry
            self.user_tweet_collection.insert_one({
                'user': user,
                'tweets': tweets
            }) 

    def store_random_tweet(self, id, tweet):
        self.global_tweet_collection.insert_one({
            'text': tweet['text']
        }) 

    def _get_unique_tweet_list(self, tweet_list):
        tweet_id_to_tweet_obj = {}
        for tweet in tweet_list:
            tweet_id = tweet['id']
            tweet_id_to_tweet_obj[tweet_id] = tweet

        unique_tweet_list = [tweet_id_to_tweet_obj[tweet_id] 
                             for tweet_id in tweet_id_to_tweet_obj]
             
        return unique_tweet_list

    def store_friends_by_screen_name(self, screen_name, friends):
        self._store_friends(screen_name, friends, self.user_friends_by_name_collection)

    def store_friends_by_id(self, id, friends):
        self._store_friends(id, friends, self.user_friends_by_id_collection)

    def _store_friends(self, user, friends, collection):
        user_doc = collection.find_one({
            'user': user
        })

        if user_doc:
            # Update
            user_doc['friends'] += friends
            user_doc['friends'] = get_unique_list(user_doc['friends'])
            collection.replace_one({
                'user': user
            }, user_doc)
        else:
            # Add new entry
            collection.insert_one({
                'user': user,
                'friends': friends
            }) 

    def store_following_by_screen_name(self, screen_name, following_users_screen_name):
        self._store_following(screen_name, following_users_screen_name, self.user_following_by_name_collection)

    def store_following_by_id(self, id, following_users_ID):
        self._store_following(id, following_users_ID, self.user_following_by_id_collection)

    def _store_following(self, user, following, collection):
        user_doc = collection.find_one({
            'user': user
        })

        if user_doc:
            # Update
            user_doc['user_following'] += following
            user_doc['user_following'] = get_unique_list(user_doc['user_following'])
            collection.replace_one({
                'user': user
            }, user_doc)
        else:
            # Add new entry
            collection.insert_one({
                'user': user,
                'user_following': following
            }) 