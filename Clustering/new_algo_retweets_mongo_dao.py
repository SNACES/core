import sys
sys.path.append('../General')
sys.path.append('../General/Concrete-DAO')

from mongoDAO import MongoDAO
from datastore import OutputDAO
from pymongo import MongoClient
from collections import Counter
import datetime
import numpy

client = MongoClient('mongodb://localhost:27017/')

class NewAlgoRetweetsMongoDAO():
    def retweet_to_id(self):
         # user list
        word_freq_db = client['WordFreq-Retweets']
        user_word_freq_collection = word_freq_db['UserRelativeWordFreq']
        user_list = []
        for doc in user_word_freq_collection.find():
            user = doc['User']
            user_list.append(user)

        db = client['productionFunction']
        collection = db['users']
        id = 0
        retweet_to_id = {}
        for user_handle in user_list:
            result = collection.find({'handle': user_handle})
            for doc in result:
                if doc['start'] == datetime.datetime(2018, 9, 1, 0, 0, 0) and\
                 doc['end'] == datetime.datetime(2019, 9, 1, 0, 0, 0) and user_handle == doc['handle']:
                    words = []

                    for tweet_text in doc['retweets']:
                        if tweet_text[0] not in retweet_to_id:
                            retweet_to_id[tweet_text[0]] = id
                            id += 1

        return retweet_to_id
    
    def user_to_tweet_id(self, retweet_to_id):
        # user list
        word_freq_db = client['WordFreq-Retweets']
        user_word_freq_collection = word_freq_db['UserRelativeWordFreq']
        user_list = []
        for doc in user_word_freq_collection.find():
            user = doc['User']
            user_list.append(user)
       
        # get user_to_tweets from database
        db = client['productionFunction']
        collection = db['users']

        user_to_tweet_id = {}
        for user_handle in user_list:
            result = collection.find({'handle': user_handle})
            for doc in result:
                if doc['start'] == datetime.datetime(2018, 9, 1, 0, 0, 0) and\
                 doc['end'] == datetime.datetime(2019, 9, 1, 0, 0, 0) and user_handle == doc['handle']:
                    words = []

                    for tweet_text in doc['retweets']:
                        if user_handle not in user_to_tweet_id:
                            user_to_tweet_id[user_handle] = []

                        retweet_id = retweet_to_id[tweet_text[0]]
                        if retweet_id not in user_to_tweet_id[user_handle]:
                            user_to_tweet_id[user_handle].append(retweet_id)

        return user_to_tweet_id

    def tweet_id_to_user(self, user_to_tweet_id):
        tweet_id_to_user = {}
        for user in user_to_tweet_id:
            for item in user_to_tweet_id[user]:
                if item not in tweet_id_to_user:
                    tweet_id_to_user[item] = []
                tweet_id_to_user[item].append(user)

        return tweet_id_to_user

        # store computed data to database
        # cluster_db = client['WordFreqClustering1']
        # important_info_collection = cluster_db['ImportantInfo']
        # important_info_collection.insert_one({
        #     "RetweetToID": retweet_to_id,
        #     "UserToItems": user_to_items,
        #     # "ItemToUsers": item_to_users
        # })

    def user_to_interaction_rate(self, user_to_retweet_id, tweet_id_to_user):
        '''
        f(y|user) = (# retweets y and user share) / sum{for each retweet of user}(the number of users for this retweet - 1)  
        '''

        user_to_interaction_rate = {}
        user_to_interaction_count = {}

        for user in user_to_retweet_id:
            user_interaction_rate = Counter()
            user_interaction_count = Counter()
            user_retweet_id_list = user_to_retweet_id[user]

            # get hash table of user_retweet_id
            user_retweet_hash = {}
            for retweet_id in user_retweet_id_list:
                user_retweet_hash[retweet_id] = 1

            # compute number of retweets y and user share
            for y in user_to_retweet_id:
                if user != y:
                    y_retweet_id_list = user_to_retweet_id[y]
                   
                    shared_retweet_count = 0
                    for retweet_id in y_retweet_id_list:
                        if retweet_id in user_retweet_hash:
                            shared_retweet_count += 1
                    
                    if shared_retweet_count != 0: 
                        user_interaction_rate[y] = shared_retweet_count
                        user_interaction_count[y] = shared_retweet_count
            
            # compute the number of retweeters in local neighborhood
            user_retweet_retweeter_count = 0
            for retweet_id in user_retweet_id_list:
                user_retweet_retweeter_count += len(tweet_id_to_user[retweet_id]) - 1
            
            # finish the user_interaction_rate computation
            for user_ in user_interaction_rate:
                user_interaction_rate[user_] /= user_retweet_retweeter_count
            
            if len(user_interaction_rate) != 0:
                user_to_interaction_rate[user] = user_interaction_rate
                user_to_interaction_count[user] = user_interaction_count
        
        return user_to_interaction_rate, user_to_interaction_count


    def user_to_global_interaction_rate(self, user_to_retweet_id, retweet_local_neighborhood_count):
        '''
        f(user) = # retweets of user / # retweets in local neighborhood
        '''
        
        user_to_global_interaction_rate = Counter()

        for user in user_to_retweet_id:
            user_to_global_interaction_rate[user] = len(user_to_retweet_id[user]) / retweet_local_neighborhood_count

        return user_to_global_interaction_rate

    def get_retweet_local_neighborhood_count(self, user_to_retweet_id):
        return sum([len(user_to_retweet_id[user]) for user in user_to_retweet_id])

    def user_to_relative_interaction_rate(self, user_to_interaction_rate, user_to_global_interaction_rate):
        user_to_relative_interaction_rate = {}
        
        for user in user_to_interaction_rate:
            user_relative_interaction_rate = Counter()
            user_interaction_rate = user_to_interaction_rate[user]
            user_global_interaction_rate = user_to_global_interaction_rate[user]

            for y in user_interaction_rate:
                user_relative_interaction_rate[y] = user_interaction_rate[y] / user_global_interaction_rate

            user_to_relative_interaction_rate[user] = user_relative_interaction_rate

        return user_to_relative_interaction_rate

    def user_to_rir_threshold_filtered(self, user_to_relative_interaction_rate, user_to_interaction_count, typicality_threshold, avg_count):
        user_to_rir_threshold_filtered = {}
        user_to_interaction_count_filtered = {}
        relevant_items = {}
        for user in user_to_relative_interaction_rate:
            filtered_user_rir = {}
            filtered_interaction_count = Counter()
            user_rir = user_to_relative_interaction_rate[user]
            average_rwf = numpy.mean(
                [rwf for item, rwf in user_rir.most_common(avg_count)])
            threshold = typicality_threshold * average_rwf
            typical_items = [interaction_user for interaction_user in user_rir if user_rir[interaction_user] > threshold]
            
            for interaction_user in typical_items:
                filtered_user_rir[interaction_user] = user_rir[interaction_user]
                filtered_interaction_count[interaction_user] = user_to_interaction_count[user][interaction_user]
                relevant_items[interaction_user] = 1

            user_to_rir_threshold_filtered[user] = filtered_user_rir
            user_to_interaction_count_filtered[user] = filtered_interaction_count

        return user_to_rir_threshold_filtered, user_to_interaction_count_filtered, relevant_items
            

    def user_to_rir_top_count_filtered(self, user_to_rir_threshold_filtered, user_to_interaction_count, top_count):
        user_to_rir_top_count_filtered = {}
        
        for user in user_to_rir_threshold_filtered:
            top_count_rir = Counter()
            rir_threshold_filtered = user_to_rir_threshold_filtered[user]

            top_count_interacted_users = user_to_interaction_count[user].most_common(top_count)
            for user_, count in top_count_interacted_users:
                top_count_rir[user_] = rir_threshold_filtered[user_]
            
            user_to_rir_top_count_filtered[user] = top_count_rir

        return user_to_rir_top_count_filtered



# store data
# retweets_popularity_only = word_freq_db['ReweetsPopularityOnly']
# for cluster in clusters:
#     retweets_popularity_only.insert_one({
#         'Users': cluster[0],
#         'Items': cluster[1]
#     })

# retweets_popularity_and_typicality = word_freq_db['RetweetsPopularityTypicality']
# for cluster in clusters:
#     retweets_popularity_and_typicality.insert_one({
#         'Users': cluster[0],
#         'Items': cluster[1]
#     })

if __name__ == '__main__':
    retweet_dao = NewAlgoRetweetsMongoDAO()
    retweet_to_id = retweet_dao.retweet_to_id()
    user_to_retweet = retweet_dao.user_to_tweet_id(retweet_to_id)
    retweet_to_user = retweet_dao.tweet_id_to_user(user_to_retweet)
    user_to_interaction_rate, user_to_interaction_count = retweet_dao.user_to_interaction_rate(user_to_retweet, retweet_to_user)
    retweet_local_neighborhood_count = retweet_dao.get_retweet_local_neighborhood_count(user_to_retweet)
    user_to_global_interaction_rate = retweet_dao.user_to_global_interaction_rate(user_to_retweet, retweet_local_neighborhood_count)
    user_to_relative_interaction_rate = retweet_dao.user_to_relative_interaction_rate(user_to_interaction_rate, user_to_global_interaction_rate)
    user_to_rir_threshold_filtered, filtered_interaction_count, _ = retweet_dao.user_to_rir_threshold_filtered(user_to_relative_interaction_rate, user_to_interaction_count, 0.5, 5)
    user_to_rir_top_count_filtered = retweet_dao.user_to_rir_top_count_filtered(user_to_rir_threshold_filtered, filtered_interaction_count, 5)
   
    print(user_to_rir_top_count_filtered['kdphd'])

