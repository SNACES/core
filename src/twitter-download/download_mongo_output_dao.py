from mongoDAO import MongoDAO
from datastore import OutputDAO

class DownloadMongoOutputDAO(MongoDAO, OutputDAO):
    def store_tweet_by_timeframe_user(self, id, start_date, end_date, tweets):
        document = {
                "id": id,
                "start_date": start_date,
                "end_date": end_date,
                # "num_tweets": num_tweets
                "tweets": tweets
            }
    
        self.collection.insert_one(document) 
    
    def store_tweet_by_user(self, id, tweets):
        document = {
                "id": id,
                # "num_tweets": num_tweets
                "tweets": tweets
            }

        self.collection.insert_one(document) 

    def store_random_tweet(self, id, tweet):
        document = {'tweetID': tweet['id'], 'text': tweet['text']}

        self.collection.insert_one(document) 

    def store_friends_by_screen_name(self, screen_name, friends):
        document = {
            "screen_name": screen_name,
            # "num_friends": num_friends,
            "friends": friends
        }

        self.collection.insert_one(document) 

    def store_friends_by_id(self, id, friends):
        document = {
            "id": id,
            # "num_friends": num_friends,
            "friends": friends
        }

        self.collection.insert_one(document) 

    def store_following_by_screen_name(self, screen_name, following_users_screen_name):
        document = {
            "screen_name": screen_name,
            "following_users_screen_name": following_users_screen_name
        }

        self.collection.insert_one(document) 

    def store_following_by_id(self, id, following_users_ID):
        document = {
            "id": id,
            "following_users_ID": following_users_ID
        }
        
        self.collection.insert_one(document) 