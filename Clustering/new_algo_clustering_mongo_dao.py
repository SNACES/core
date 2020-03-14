import sys
sys.path.append('../General')
sys.path.append('../General/Concrete-DAO')

from mongoDAO import MongoDAO
from datastore import OutputDAO
from pymongo import MongoClient
from collections import Counter
import numpy

client = MongoClient('mongodb://localhost:27017/')

class NewAlgoClusteringMongoDAO():   
    def get_rwf(self):
        # get user_to_rwf from database
        word_freq_db = client['WordFreq-Test2']
        user_relative_word_freq_collection = word_freq_db['UserRWF']
        user_word_freq_collection = word_freq_db["UserWordFreq"]
        user_to_rwf = {}
        for doc in user_relative_word_freq_collection.find():
            user = doc['User']
            rwf_vector = Counter(doc['RelativeWordFrequency'])
            new_rwf_vector = Counter()
            # words_not_in_wf_vector = doc['UserWordsNotInGlobal']

            # # compute modified user relative wf
            # if modified_wf_vector != {}:  # TODO: careful about this corner case
            #     word_count_doc = user_word_freq_collection.find({"User": user})[0]
            #     user_word_frequency = word_count_doc['UserWordFreqVector']
            #     for word in words_not_in_wf_vector:
            #         word_count = user_word_frequency[word]
            #         modified_wf_vector[word] = word_count / \
            #             20000  # TODO: this is hardcoded for now
            #     # get 50 of the most common words
            #     final_wf_vector = Counter()
            #     for item in modified_wf_vector.most_common():
            #         final_wf_vector[item[0]] = item[1]

            #     user_to_rwf[user] = final_wf_vector
            if rwf_vector != {}:
                for word, value in rwf_vector.most_common(): # 50
                    new_rwf_vector[word] = value
                user_to_rwf[user] = new_rwf_vector 

        return user_to_rwf

    def get_user_to_info(self, user_to_rwf):
        """ 
        # >>> rwf = dao.get_rwf()
        # >>> table1 = dao.get_user_to_info(rwf)
        # >>> print(table1)
        
        {
            Table 1
            user : {word : (rwf, count)}
        }
        """
        
        word_freq_db = client['WordFreq-Test2']
        user_relative_word_freq_collection = word_freq_db['UserRWF']
        user_word_freq_collection = word_freq_db["UserWordFreq"]
        user_to_info = {}

        for user in user_to_rwf:
            user_info = {}
            user_rwf = user_to_rwf[user]
            user_wf = user_word_freq_collection.find({"User": user})[0]['UserWordFreqVector']
            for word in user_rwf:
                rwf = user_rwf[word]
                count = user_wf[word]
                user_info[word] = (rwf, count)
            user_to_info[user] = user_info

        return user_to_info


    def get_filtered_user_to_info(self, user_to_info, factor, count):
        """ 
        # >>> rwf = dao.get_rwf()
        # >>> table1 = dao.get_user_to_info(rwf)
        # >>> table2, _ = dao.get_filtered_user_to_info(table1, 0.5, 5)
        # >>> print(table2)

        {
            Table 2
            user : {word : (rwf, count)}
        }
        """

        return self.get_filtered(user_to_info, factor, count)
        
    def get_filtered(self, user_to_info, factor, count):
        filtered_user_to_info = {}
        relevant_words = {}
        for user in user_to_info:
            filtered_user_info = {}
            user_info = user_to_info[user]
            user_rwf = Counter({word:user_info[word][0] for word in user_info})
            average_rwf = numpy.mean(
                [rwf for item, rwf in user_rwf.most_common(count)])
            threshold = factor * average_rwf
            typical_items = [word for word in user_rwf if user_rwf[word] > threshold]
            for word in typical_items:
                filtered_user_info[word] = user_info[word]
                relevant_words[word] = 1

            filtered_user_to_info[user] = filtered_user_info

        return filtered_user_to_info, relevant_words

    def get_item_to_info(self, filtered_user_to_info, relevant_words):
        """
        {
            Table 3
            word : {user : (rwf, count)}
        }
        
        # >>> rwf = dao.get_rwf()
        # >>> table1 = dao.get_user_to_info(rwf)
        # >>> table2, relevant_words = dao.get_filtered_user_to_info(table1, 0.5, 5)
        # >>> table3 = dao.get_item_to_info(table2, relevant_words)
        # >>> print(table3)
        """

        item_to_info = {}
        for user in filtered_user_to_info:
            for item in filtered_user_to_info[user]:
                if item not in item_to_info:
                    item_to_info[item] = {}
                info = filtered_user_to_info[user][item]
                item_to_info[item][user] = info

        return item_to_info
        
    def get_filtered_item_to_info(self, item_to_info, factor, count):
        """
        {
            Table 4
            Filter based on avg threshold for top x
            word : {user : (rwf, count)}
        }

        # >>> factor, count = 0.5, 5
        # >>> rwf = dao.get_rwf()
        # >>> table1 = dao.get_user_to_info(rwf)
        # >>> table2, relevant_words = dao.get_filtered_user_to_info(table1, factor, count)
        # >>> table3 = dao.get_item_to_info(table2, relevant_words)
        # >>> table4, relevant_users = dao.get_filtered_item_to_info(table3, factor, count)
        # >>> print(relevant_users)
        """
        
        # want to get the most typical users for each word
        # for each word, get the average rwf among users of this word, then filter users by threshold
        return self.get_filtered(item_to_info, factor, count)

    def get_item_to_users(self, filtered_item_to_info, top_count):
        """
        {
            Table 5
            Use table 4: for each word, get top x users by word count
            word : {user : (rwf, count)}
        }
        
        # >>> factor, count = 0.5, 5
        # >>> rwf = dao.get_rwf()
        # >>> table1 = dao.get_user_to_info(rwf)
        # >>> table2, relevant_words = dao.get_filtered_user_to_info(table1, factor, count)
        # >>> table3 = dao.get_item_to_info(table2, relevant_words)
        # >>> table4, relevant_users = dao.get_filtered_item_to_info(table3, factor, count)
        # >>> table5 = dao.get_item_to_users(table4, 5)
        # >>> print(table5)
        """

        return self.get_top_count(filtered_item_to_info, top_count)

    def get_top_count(self, filtered_item_to_info, top_count):
        item_to_users = {}
        for word in filtered_item_to_info:
            final_item_info = {}
            item_info = filtered_item_to_info[word]

            # get only the top x users by word count
            user_count = Counter({user: item_info[user][1] for user in item_info})
            top_users = [user for user, count in user_count.most_common(top_count)]
            for user in top_users:
                final_item_info[user] = item_info[user]
            item_to_users[word] = final_item_info

        return item_to_users

    def get_double_filter_user_to_info(self, filtered_user_to_info, relevant_users):
        """
        {
            Table 6
            Filter user_to_info even more so that users only are from item to users
            user : {word : (rwf, count)}
        }

        # >>> factor, count = 0.5, 5
        # >>> rwf = dao.get_rwf()
        # >>> table1 = dao.get_user_to_info(rwf)
        # >>> table2, relevant_words = dao.get_filtered_user_to_info(table1, factor, count)
        # >>> table3 = dao.get_item_to_info(table2, relevant_words)
        # >>> table4, relevant_users = dao.get_filtered_item_to_info(table3, factor, count)
        # >>> table6 = dao.get_double_filter_user_to_info(table2, relevant_users)
        # >>> print(table6)
        """
        
        return {user:filtered_user_to_info[user] for user in relevant_users}

    def get_user_to_items(self, double_filter_user_to_info, top_count):
        """
        {
            Table 7
            Filter table 6 so that we only items are the top items by count
            user : {word : (rwf, count)} maybe we also want a version that doesn't have count
        }

        # >>> factor, count = 0.5, 5
        # >>> rwf = dao.get_rwf()
        # >>> table1 = dao.get_user_to_info(rwf)
        # >>> table2, relevant_words = dao.get_filtered_user_to_info(table1, factor, count)
        # >>> table3 = dao.get_item_to_info(table2, relevant_words)
        # >>> table4, relevant_users = dao.get_filtered_item_to_info(table3, factor, count)
        # >>> table6 = dao.get_double_filter_user_to_info(table2, relevant_users)
        # >>> table7 = dao.get_user_to_items(table6, 5)
        # >>> print(table7)
        """

        return self.get_top_count(double_filter_user_to_info, top_count)


    def store_clusters(self, clusters, threshold, user_count, item_count):
        word_freq_db = client['WordFreqClusteringNoiseTestsAllWords']
        user_tweets_popularity_only = word_freq_db['UserTweetsOnlyPopularity']
        user_tweets_popularity_only.insert_one({
            'Threshold': threshold,
            'UserCount': user_count,
            'ItemCount': item_count,
            'Clusters': clusters
        })


    def user_to_items(self, table6, factor, item_count):
      
        table7 = self.get_user_to_items(table6, item_count)

        return {user:Counter({item:table6[user][item][0] for item in table7[user]}) for user in table7}

    def item_to_users(self, table4, factor, user_count):
        table5 = self.get_item_to_users(table4, user_count)

        return {item:Counter({user:table4[item][user][0] for user in table5[item]}) for item in table5}
        
        
# testing
import doctest
doctest.testmod(extraglobs={'dao': NewAlgoClusteringMongoDAO()})
