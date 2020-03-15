from new_algo_clustering import *
from new_algo_clustering_mongo_dao import *
import daemon
from collections import Counter, OrderedDict
import operator

# -------------------------------User Tweets------------------------------------
def run_clustering_experiment(rwf, threshold, user_count, item_count, intersection_min, popularity):
    # get user_to_items
    user_to_items = dao.user_to_items(table2, threshold, item_count)

    # get item_to_users
    item_to_users = dao.item_to_users(table4, threshold, user_count)

    # call detect all communities
    clusters = new_algo_clustering.detect_all_communities(user_to_items, item_to_users, user_count, item_count, intersection_min, popularity, True)

    # get the most typical words for each cluster
    for cluster in clusters:
        cluster_rwf = cluster_relative_frequency(rwf, cluster['users'])
        most_typical_words = []
        for item in cluster_rwf.most_common(10):
            most_typical_words.append(item[0])
        most_typical_words.sort()
        cluster['typical'] = most_typical_words

    return clusters

def save_to_file(file_name, cluster_list):
    file_object = open(file_name, 'w')
    sorted_cluster_list = sorted(cluster_list, key = lambda cluster : cluster['count'], reverse=True)
    for cluster in sorted_cluster_list:
        core_users = cluster['users']
        core_items = cluster['items']
        most_typical_words = cluster['typical']
        duplicate_count = cluster['count']
        file_object.write("Core Users: {}\nCore Items: {}\nMost Typical Words: {}\nDuplicate Count: {}\n\n".format(core_users, core_items, most_typical_words, duplicate_count)) # TODO:

with daemon.DaemonContext(chroot_directory=None, working_directory='./'):
    intersection_min_list = [5, 4, 3, 2]
    popularity_list = [0.3, 0.2]
    threshold_list = [0.7, 0.5, 0.3, 0.2, 0.1]
    top_items = [5, 10, 15, 20, 25, 30]
    top_users = [5, 10, 15]

    # intersection_min = 5
    # threshold_list = [0.1, 0.3]
    # top_items = [20, 25, 30]
    # top_users = [5, 15]
    new_algo_clustering = NewAlgoClustering()
    dao = NewAlgoClusteringMongoDAO()
    rwf = dao.get_rwf()
    table1 = dao.get_user_to_info(rwf)

    # threshold = 0.1
    # table2, relevant_words = dao.get_filtered_user_to_info(table1, threshold, 5)
    # table3 = dao.get_item_to_info(table2, relevant_words)
    # table4, relevant_users = dao.get_filtered_item_to_info(table3, threshold, 5)
    # table6 = dao.get_double_filter_user_to_info(table2, relevant_users)
    # print(table6['JFutoma'])

    for intersection_min in intersection_min_list:
        for popularity in popularity_list:
            for threshold in threshold_list:
                table2, relevant_words = dao.get_filtered_user_to_info(table1, threshold, 5)
                table3 = dao.get_item_to_info(table2, relevant_words)
                table4, relevant_users = dao.get_filtered_item_to_info(table3, threshold, 5)
                table6 = dao.get_double_filter_user_to_info(table2, relevant_users)
                for user_count in top_users:
                    for item_count in top_items:
                        clusters = run_clustering_experiment(rwf, threshold, user_count, item_count, intersection_min, popularity)
                        
                        # save results to file and database
                        file_name = "Popularity {} Intersection Min {} Threshold {}, Top Items {}, Top Users {}".format(popularity, intersection_min, threshold, item_count, user_count)
                        save_to_file(file_name, clusters)
#                         dao.store_clusters(clusters, threshold, user_count, item_count)

# ----------------------------------Retweets------------------------------------
# compute retweet to id map

# user list
# word_freq_db = client['WordFreq-Retweets']
# user_word_freq_collection = word_freq_db['UserRelativeWordFreq']
# user_list = []
# for doc in user_word_freq_collection.find():
#     user = doc['User']
#     user_list.append(user)

# db = client['productionFunction']
# collection = db['users']
# id = 0
# retweet_to_id = {}
# for user_handle in user_list:
#     result = collection.find({'handle': user_handle})
#     for doc in result:
#         if doc['start'] == datetime.datetime(2018, 9, 1, 0, 0, 0) and\
#          doc['end'] == datetime.datetime(2019, 9, 1, 0, 0, 0) and user_handle == doc['handle']:
#             words = []

#             for tweet_text in doc['retweets']:
#                 if tweet_text[0] not in retweet_to_id:
#                     retweet_to_id[tweet_text[0]] = id
#                     id += 1


# # get user_to_items from database
# user_to_items = {}
# for user_handle in user_list:
#     result = collection.find({'handle': user_handle})
#     for doc in result:
#         if doc['start'] == datetime.datetime(2018, 9, 1, 0, 0, 0) and\
#          doc['end'] == datetime.datetime(2019, 9, 1, 0, 0, 0) and user_handle == doc['handle']:
#             words = []

#             for tweet_text in doc['retweets']:
#                 if user_handle not in user_to_items:
#                     user_to_items[user_handle] = []

#                 retweet_id = retweet_to_id[tweet_text[0]]
#                 user_to_items[user_handle].append(retweet_id)

# # compute item_to_users
# item_to_users = {}
# for user in user_to_items:
#     for item in user_to_items[user]:
#         if item not in item_to_users:
#             item_to_users[item] = []
#         item_to_users[item].append(user)

# store computed data to database
# cluster_db = client['WordFreqClustering1']
# important_info_collection = cluster_db['ImportantInfo']
# important_info_collection.insert_one({
#     "RetweetToID": retweet_to_id,
#     "UserToItems": user_to_items,
#     # "ItemToUsers": item_to_users
# })


# print(retweet_to_id)

# call detect all communities
# clusters = detect_all_communities(user_to_items, item_to_users, False)

# ids = [479, 480, 481, 482, 484]
# for tweet in retweet_to_id:
#     if retweet_to_id[tweet] in ids:
#         print("Tweet ID: " + str(retweet_to_id[tweet]) + " Tweet: " + tweet)


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





'''
TODO:
- compute user_to_items and item_to_users for retweets, then run clustering algo and store
- do this but without limits on user pairs


store item to user, so don't need to recompute, same for user to items
get top 50 words for each user
store ordered, so that don't need to reorder

want to compare the results >> pop vs pop and typ look too different >> for retweets, even worse cuz no words
suggestion for comp >> if given a set of users, compute for cluster relative word freq and take the top 10 words >> kinda like affinity >> do for both retweet and tweet and compare words

why so different? >> understand wuz goin on
make sure programming good
then run experiments >> like top 10 >> change parameters

 mongoexport --db WordFreqClustering1 --collection UserTweetsOnlyPopularity | sed '/"_id":/s/"_id":[^,]*,//' > user_tweets_popularity_only.json


**** fix issue with random tweet downloader
'''

# f = open('UserRWF', 'w')
# word_freq_db = client['WordFreq-Test2']
# user_relative_word_freq_collection = word_freq_db['UserRWF']
# user_word_freq_collection = word_freq_db["UserWordFreq"]
# for doc in user_relative_word_freq_collection.find():
#     user = doc['User']
#     orig_rwf_vector = Counter(doc['RelativeWordFrequency'])
    
#     f.write("User: {}\nRWF: {}\n\n".format(user, orig_rwf_vector))





# word_freq_db = client['WordFreq-Test2']
# user_relative_word_freq_collection = word_freq_db['UserRelativeWordFreq']
# user_word_freq_collection = word_freq_db["UserWordFreq"]

# new_algo_clustering = NewAlgoClustering()
# dao = NewAlgoClusteringMongoDAO()
# rwf = dao.get_rwf()
# table1 = dao.get_user_to_info(rwf)

# for threshold in [0.7, 0.5, 0.3, 0.2, 0.1]:
#     table2, relevant_words = dao.get_filtered_user_to_info(table1, threshold, 5)
#     table3 = dao.get_item_to_info(table2, relevant_words)
#     table4, relevant_users = dao.get_filtered_item_to_info(table3, threshold, 5)
#     table6 = dao.get_double_filter_user_to_info(table2, relevant_users)
#     table7 = dao.get_user_to_items(table6, 10)

#     # f = open('UserToItems Threshold {}'.format(threshold), 'w')
#     # for user in ['JFutoma', 'david_sontag', 'Yair_Rosenberg', 'dhackett1565', 'random_walker', 'GraphicMatt']:
#     #     f.write("{}\n".format(user))
#     #     # f.write("Table 1(Top 50 Words by RWF): {}\n".format(table1[user]))
#     #     f.write("Table 2(Threshold Filtered): {}\n".format(table2[user]))
#     #     f.write("Table 6(Words only from Table 4): {}\n".format(table6[user]))
#     #     f.write("Table 7(Top 5 Words by Word Count): {}\n\n".format(table7[user]))

#     f = open('Item to Users(Table 4) Threshold {}'.format(threshold), 'w')
#     for word in ['rl', 'ml', 'algorithm', 'partisan', 'infosec', 'raptor', 'ttc']:
#         result = table4[word]
#         # sorted(result, key = lambda cluster : cluster['count'], reverse=True)
#         result = sorted(result.items(), key=lambda x: x[1][0], reverse=True)
#         f.write("{}\n".format(word))
#         f.write("{}\n\n".format(result))