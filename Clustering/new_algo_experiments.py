from new_algo_clustering import *
from new_algo_clustering_mongo_dao import *
from new_algo_retweets_mongo_dao import *
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

# with daemon.DaemonContext(chroot_directory=None, working_directory='./'):
#     intersection_min_list = [5, 4, 3, 2]
#     popularity_list = [0.3, 0.2]
#     threshold_list = [0.7, 0.5, 0.3, 0.2, 0.1]
#     top_items = [5, 10, 15, 20, 25, 30]
#     top_users = [5, 10, 15]

#     # intersection_min = 5
#     # threshold_list = [0.1, 0.3]
#     # top_items = [20, 25, 30]
#     # top_users = [5, 15]
#     new_algo_clustering = NewAlgoClustering()
#     dao = NewAlgoClusteringMongoDAO()
#     rwf = dao.get_rwf()
#     table1 = dao.get_user_to_info(rwf)

#     # threshold = 0.1
#     # table2, relevant_words = dao.get_filtered_user_to_info(table1, threshold, 5)
#     # table3 = dao.get_item_to_info(table2, relevant_words)
#     # table4, relevant_users = dao.get_filtered_item_to_info(table3, threshold, 5)
#     # table6 = dao.get_double_filter_user_to_info(table2, relevant_users)
#     # print(table6['JFutoma'])

#     for intersection_min in intersection_min_list:
#         for popularity in popularity_list:
#             for threshold in threshold_list:
#                 table2, relevant_words = dao.get_filtered_user_to_info(table1, threshold, 5)
#                 table3 = dao.get_item_to_info(table2, relevant_words)
#                 table4, relevant_users = dao.get_filtered_item_to_info(table3, threshold, 5)
#                 table6 = dao.get_double_filter_user_to_info(table2, relevant_users)
#                 for user_count in top_users:
#                     for item_count in top_items:
#                         clusters = run_clustering_experiment(rwf, threshold, user_count, item_count, intersection_min, popularity)
                        
#                         # save results to file and database
#                         file_name = "Popularity {} Intersection Min {} Threshold {}, Top Items {}, Top Users {}".format(popularity, intersection_min, threshold, item_count, user_count)
#                         save_to_file(file_name, clusters)
# #                         dao.store_clusters(clusters, threshold, user_count, item_count)

# ----------------------------------Retweets------------------------------------
retweet_dao = NewAlgoRetweetsMongoDAO()
retweet_to_id = retweet_dao.retweet_to_id()
user_to_retweet = retweet_dao.user_to_tweet_id(retweet_to_id)
retweet_to_user = retweet_dao.tweet_id_to_user(user_to_retweet)
user_to_interaction_rate, user_to_interaction_count = retweet_dao.user_to_interaction_rate(user_to_retweet, retweet_to_user)
retweet_local_neighborhood_count = retweet_dao.get_retweet_local_neighborhood_count(user_to_retweet)
user_to_global_interaction_rate = retweet_dao.user_to_global_interaction_rate(user_to_retweet, retweet_local_neighborhood_count)
user_to_relative_interaction_rate = retweet_dao.user_to_relative_interaction_rate(user_to_interaction_rate, user_to_global_interaction_rate)

new_algo_clustering = NewAlgoClustering()
dao = NewAlgoClusteringMongoDAO()
rwf = dao.get_rwf()

# user_count = 5
# item_count = 5
# intersection_min = 2
# popularity = 0.3


intersection_min_list = [3, 2]
popularity_list = [0.3]
threshold_list = [0.7, 0.5, 0.3, 0.2, 0.1]
top_items = [5, 10, 15]
top_users = [5, 10, 15]

# with daemon.DaemonContext(chroot_directory=None, working_directory='./'):
for intersection_min in intersection_min_list:
    for popularity in popularity_list:
        for typicality_threshold in threshold_list:
            user_to_rir_threshold_filtered, filtered_interaction_count, _ = retweet_dao.user_to_rir_threshold_filtered(user_to_relative_interaction_rate, user_to_interaction_count, typicality_threshold, 5)
            user_to_rir_top_count_filtered = retweet_dao.user_to_rir_top_count_filtered(user_to_rir_threshold_filtered, filtered_interaction_count, 5)

            for user_count in top_users:
                for item_count in top_items:
                    cluster_list = new_algo_clustering.detect_all_communities(user_to_rir_top_count_filtered, user_to_rir_top_count_filtered, user_count, item_count, intersection_min, popularity, True)
                    print(cluster_list)
                    # get the most typical words for each cluster
                    for cluster in cluster_list:
                        cluster_rwf = cluster_relative_frequency(rwf, cluster['users'])
                        most_typical_words = []
                        for item in cluster_rwf.most_common(10):
                            most_typical_words.append(item[0])
                        most_typical_words.sort()
                        cluster['typical'] = most_typical_words

                    
                    # save results to file and database
                    file_name = "Popularity {} Intersection Min {} Threshold {}, Top Items {}, Top Users {}".format(popularity, intersection_min, typicality_threshold, item_count, user_count)
                    save_to_file(file_name, cluster_list)
                    # dao.store_clusters(clusters, threshold, user_count, item_count)


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