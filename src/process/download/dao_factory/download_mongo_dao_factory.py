from src.shared.mongo import get_collection_from_config
from src.datastore.mongo.raw_tweet.tweet_mongo_set import TweetMongoSetDAO
from src.datastore.mongo.user_friend.user_friends_mongo_set import UserFriendsMongoSetDAO
from src.datastore.mongo.user_follower.user_followers_mongo_set import UserFollowersMongoSetDAO

class DownloadMongoDAOFactory():
    def create_tweet_setter(self, tweet_config):
        tweet_mongo_setter = TweetMongoSetDAO()

        global_tweets_config = tweet_config['Global-Tweet'] if 'Global-Tweet' in tweet_config else None
        user_tweets_config = tweet_config['User-Tweet'] if 'User-Tweet' in tweet_config else None

        # Get Global Tweets
        if global_tweets_config:
            tweet_mongo_setter.global_tweet_collection = get_collection_from_config(global_tweets_config)

        # Get User Tweets
        if user_tweets_config:
            tweet_mongo_setter.user_tweet_collection = get_collection_from_config(user_tweets_config)

        if not global_tweets_config and not user_tweets_config:
            tweet_mongo_setter = None

        return tweet_mongo_setter

    def create_user_friends_setter(self, user_friends_config):
        user_friends_setter = UserFriendsMongoSetDAO()

        by_name_config = user_friends_config['User-Friend-By-Name'] if 'User-Friend-By-Name' in user_friends_config else None
        by_id_config = user_friends_config['User-Friend-By-ID'] if 'User-Friend-By-ID' in user_friends_config else None 

        if by_name_config:
            user_friends_setter.user_friends_by_name_collection = get_collection_from_config(by_name_config)
  
        if by_id_config:
            user_friends_setter.user_friends_by_id_collection = get_collection_from_config(by_id_config)

        if not by_name_config and not by_id_config:
            user_friends_setter = None

        return user_friends_setter

    def create_user_followers_setter(self, user_followers_config):
        user_followers_setter = UserFollowersMongoSetDAO()

        by_name_config = user_followers_config['User-Follower-By-Name'] if 'User-Follower-By-Name' in user_followers_config else None
        by_id_config = user_followers_config['User-Follower-By-ID'] if 'User-Follower-By-ID' in user_followers_config else None 

        if by_name_config:
            user_followers_setter.user_followers_by_name_collection = get_collection_from_config(by_name_config)
  
        if by_id_config:
            user_followers_setter.user_followers_by_id_collection = get_collection_from_config(by_id_config)

        if not by_name_config and not by_id_config:
            user_followers_setter = None

        return user_followers_setter