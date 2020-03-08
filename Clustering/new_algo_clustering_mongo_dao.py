import sys
sys.path.append('../General')
sys.path.append('../General/Concrete-DAO')

from mongoDAO import MongoDAO
from datastore import OutputDAO
from pymongo import MongoClient
from collections import Counter

client = MongoClient('mongodb://localhost:27017/')

class NewAlgoClusteringMongoDAO():
    def get_rwf(self):
        # get user_to_rwf from database
        word_freq_db = client['WordFreq-Test2']
        user_relative_word_freq_collection = word_freq_db['UserRelativeWordFreq']
        user_word_freq_collection = word_freq_db["UserWordFreq"]
        user_to_rwf = {}
        for doc in user_relative_word_freq_collection.find():
            user = doc['User']
            modified_wf_vector = Counter(doc['RelativeWordFrequency'])
            words_not_in_wf_vector = doc['UserWordsNotInGlobal']

            # compute modified user relative wf
            if modified_wf_vector != {}:  # TODO: careful about this corner case
                word_count_doc = user_word_freq_collection.find({"User": user})[0]
                user_word_frequency = word_count_doc['UserWordFreqVector']
                for word in words_not_in_wf_vector:
                    word_count = user_word_frequency[word]
                    modified_wf_vector[word] = word_count / \
                        20000  # TODO: this is hardcoded for now
                # get 50 of the most common words
                final_wf_vector = Counter()
                for item in modified_wf_vector.most_common(50):
                    final_wf_vector[item[0]] = item[1]

                user_to_rwf[user] = final_wf_vector

        return user_to_rwf

    def store_clusters(self, clusters, threshold, user_count, item_count):
        word_freq_db = client['WordFreqClustering']
        user_tweets_popularity_only = word_freq_db['UserTweetsOnlyPopularity']
        user_tweets_popularity_only.insert_one({
            'Threshold': threshold,
            'UserCount': user_count,
            'ItemCount': item_count,
            'Clusters': clusters
        })


    def get_s(self):
        pass
