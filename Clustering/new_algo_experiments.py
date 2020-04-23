from new_algo_clustering import *
from new_algo_clustering_mongo_dao import *
from new_algo_retweets_clustering import *
from new_algo_retweets_mongo_dao import *
import daemon
from collections import Counter, OrderedDict
import operator
import parse
import numpy

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

def save_to_file_words(file_name, cluster_list):
    file_object = open(file_name, 'w')
    sorted_cluster_list = sorted(cluster_list, key = lambda cluster : cluster['count'], reverse=True)
    for cluster in sorted_cluster_list:
        core_users = cluster['users']
        core_items = cluster['items']
        most_typical_words = cluster['typical']
        duplicate_count = cluster['count']

        cluster_info = "Core Users: {}\nCore Items: {}\nMost Typical Words: {}\nDuplicate Count: {}\n\n".format(core_users, core_items, most_typical_words, duplicate_count)
        file_object.write(cluster_info) 

def save_to_file_retweets(file_name, cluster_list):
    file_object = open(file_name, 'w')
    sorted_cluster_list = sorted(cluster_list, key = lambda cluster : cluster['count'], reverse=True)
    for cluster in sorted_cluster_list:
        core_users = cluster['users']
        most_typical_words = cluster['typical']
        duplicate_count = cluster['count']

        if 'shared_retweet_avg' in cluster:
            shared_retweet_avg = cluster['shared_retweet_avg']
            cluster_info = "Core Users: {}\nMost Typical Words: {}\nDuplicate Count: {}\nShared Retweet Average: {}\n\n".format(core_users, most_typical_words, duplicate_count, shared_retweet_avg)
        else:
            cluster_info = "Core Users: {}\nMost Typical Words: {}\nDuplicate Count: {}\n\n".format(core_users, most_typical_words, duplicate_count)
        file_object.write(cluster_info) 

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

# ------------------------User Tweets Post-Processing---------------------------
def get_cluster_list_from_file(file_name):
    file_object = open(file_name, 'r')
    cluster_list = []
    cluster_txt_data = file_object.read()
    cluster_txt_data_list = cluster_txt_data.split('\n\n')

    for cluster_txt_data in cluster_txt_data_list:
        if cluster_txt_data != "":
            format_str = "Core Users: {}\nCore Items: {}\nMost Typical Words: {}\nDuplicate Count: {}"
            cluster_info = parse.parse(format_str, cluster_txt_data)
            # print(cluster_info)

            core_users = list(eval(cluster_info[0]))
            core_items = list(eval(cluster_info[1]))
            most_typical_words = list(eval(cluster_info[2]))
            duplicate_count = int(cluster_info[3])

            cluster = {}
            cluster['users'] = core_users
            cluster['items'] = core_items
            cluster['typical'] = most_typical_words 
            cluster['count'] = duplicate_count
            cluster_list.append(cluster)

    return cluster_list

def is_satisfy_commonality(li1, li2, commonality_threshold):
    len_threshold = int(min(len(li1), len(li2)) * commonality_threshold)
    return len(set(li1).intersection(set(li2))) >= len_threshold

def merge(lists, commonality_threshold, results=None):
    if results is None:
        results = []

    if not lists:
        return results

    first = lists[0]
    # merged_words = []
    # merged_users = []
    # merged_count = 0
    output = []

    for li in lists[1:]:
        if is_satisfy_commonality(li['items'], first['items'], commonality_threshold):
            # merged_words += li['typical']
            # merged_users += li['users']
            # merged_count += li['count']
            
            first['typical'] += li['typical']
            first['items'] += li['items']
            first['users'] += li['users']
            first['count'] += li['count']
        else:
            output.append(li)

    # remove duplicate elements in typical item and user lists
    first['typical'] = list(dict.fromkeys(first['typical']))
    first['items'] = list(dict.fromkeys(first['items']))
    first['users'] = list(dict.fromkeys(first['users']))

    results.append(first)

    return merge(output, commonality_threshold, results)

intersection_min_list = [3, 2]
popularity_list = [0.3]
threshold_list = [0.7, 0.5, 0.3, 0.1]
top_items = [5, 10, 15]
top_users = [5, 10, 15]
commonality_threshold_list = [0.75, 0.5]
for commonality_threshold in commonality_threshold_list:
    for intersection_min in intersection_min_list:
        for popularity in popularity_list:
            for typicality_threshold in threshold_list:
                for user_count in top_users:
                    for item_count in top_items:
                        # file_name = "Threshold {}, Top Items {}, Top Users {}".format(typicality_threshold, item_count, user_count)
                        # new_file_name = "Popularity {} Intersection Min {} Threshold {}, Top Items {}, Top Users {}".format(popularity, intersection_min, typicality_threshold, item_count, user_count)
                        
                        file_name = "Popularity {} Intersection Min {} Threshold {}, Top Items {}, Top Users {}".format(popularity, intersection_min, typicality_threshold, item_count, user_count)
                        new_file_name = "Commonality {} Popularity {} Intersection Min {} Threshold {}, Top Items {}, Top Users {}".format(commonality_threshold, popularity, intersection_min, typicality_threshold, item_count, user_count)
                        
                        cluster_list = get_cluster_list_from_file(file_name)

                        # merge clusters that are too similar
                        cluster_list = merge(cluster_list, commonality_threshold)
                        
                        save_to_file_words(new_file_name, cluster_list)


# ----------------------------------Retweets------------------------------------
retweet_dao = NewAlgoRetweetsMongoDAO()
retweet_to_id = retweet_dao.retweet_to_id()
user_to_retweet = retweet_dao.user_to_tweet_id(retweet_to_id)
retweet_to_user = retweet_dao.tweet_id_to_user(user_to_retweet)
user_to_interaction_rate, user_to_interaction_count = retweet_dao.user_to_interaction_rate(user_to_retweet, retweet_to_user)
retweet_local_neighborhood_count = retweet_dao.get_retweet_local_neighborhood_count(user_to_retweet)
user_to_global_interaction_rate = retweet_dao.user_to_global_interaction_rate(user_to_retweet, retweet_local_neighborhood_count)
user_to_relative_interaction_rate = retweet_dao.user_to_relative_interaction_rate(user_to_interaction_rate, user_to_global_interaction_rate)

new_algo_clustering = NewAlgoRetweetsClustering()
dao = NewAlgoClusteringMongoDAO()
rwf = dao.get_rwf()

intersection_min_list = [3, 2]
popularity_list = [0.3]
threshold_list = [0.7, 0.5, 0.3, 0.2, 0.1]
top_items = [5, 10, 15]
top_users = [5, 10, 15]

# with daemon.DaemonContext(chroot_directory=None, working_directory='./'):
# for intersection_min in intersection_min_list:
#     for popularity in popularity_list:
#         for typicality_threshold in threshold_list:
#             user_to_rir_threshold_filtered, filtered_interaction_count, _ = retweet_dao.user_to_rir_threshold_filtered(user_to_relative_interaction_rate, user_to_interaction_count, typicality_threshold, 5)

#             for user_count in top_users:
#                 for item_count in top_items:
#                     user_to_rir_top_count_filtered = retweet_dao.user_to_rir_top_count_filtered(user_to_rir_threshold_filtered, filtered_interaction_count, item_count)
#                     cluster_list = new_algo_clustering.detect_all_communities(user_to_rir_top_count_filtered, user_count, intersection_min, popularity)
#                     # get the most typical words for each cluster
#                     for cluster in cluster_list:
#                         cluster_rwf = cluster_relative_frequency(rwf, cluster['users'])
#                         most_typical_words = []
#                         for item in cluster_rwf.most_common(10):
#                             most_typical_words.append(item[0])
#                         most_typical_words.sort()
#                         cluster['typical'] = most_typical_words

#                     # save results to file and database
#                     file_name = "Popularity {} Intersection Min {} Threshold {}, Top Items {}, Top Users {}".format(popularity, intersection_min, typicality_threshold, item_count, user_count)
#                     save_to_file_retweets(file_name, cluster_list)
#                     # dao.store_clusters(clusters, threshold, user_count, item_count)

# ---------------------------Retweets Post-Processing---------------------------

# def get_cluster_list_from_file(file_name):
#     file_object = open(file_name, 'r')
#     cluster_list = []
#     cluster_txt_data = file_object.read()
#     cluster_txt_data_list = cluster_txt_data.split('\n\n')

#     for cluster_txt_data in cluster_txt_data_list:
#         if cluster_txt_data != "":
#             # format_str = "Core Users: {}\nMost Typical Words: {}\nDuplicate Count: {}"
#             format_str = "Core Users: {}\nMost Typical Words: {}\nDuplicate Count: {}\nShared Retweet Average: {}"
            
#             cluster_info = parse.parse(format_str, cluster_txt_data)
            
#             # print(cluster_info)

#             core_users = list(eval(cluster_info[0]))
#             most_typical_words = list(eval(cluster_info[1]))
#             duplicate_count = int(cluster_info[2])


#             cluster = {}
#             cluster['users'] = core_users
#             cluster['typical'] = most_typical_words 
#             cluster['count'] = duplicate_count
#             cluster_list.append(cluster)

#     return cluster_list

# def is_satisfy_commonality(li1, li2, commonality_threshold):
#     len_threshold = int(min(len(li1), len(li2)) * commonality_threshold)
#     return len(set(li1).intersection(set(li2))) >= len_threshold

# def merge(lists, commonality_threshold, results=None):
#     if results is None:
#         results = []

#     if not lists:
#         return results

#     first = lists[0]
#     # merged_words = []
#     # merged_users = []
#     # merged_count = 0
#     output = []

#     for li in lists[1:]:
#         if is_satisfy_commonality(li['typical'], first['typical'], commonality_threshold):
#             # merged_words += li['typical']
#             # merged_users += li['users']
#             # merged_count += li['count']
            
#             first['typical'] += li['typical']
#             first['users'] += li['users']
#             first['count'] += li['count']
#         else:
#             output.append(li)

#     # merged_words += first['typical']
#     # merged_users += first['users']
#     # merged_count += first['count']

#     results.append(first)

#     return merge(output, commonality_threshold, results)

# def compute_cluster_retweet_average(cluster_list, user_to_interaction_count):
#     for i in range(len(cluster_list)):
#         cluster = cluster_list[i]
#         pair_interaction_list = []
#         for user1 in cluster['users']:
#             for user2 in cluster['users']:
#                 if user1 != user2:
#                     interaction_count = user_to_interaction_count[user1][user2]
#                     pair_interaction_list.append(interaction_count)

#         cluster['shared_retweet_avg'] = numpy.mean(pair_interaction_list)


# for intersection_min in intersection_min_list:
#     for popularity in popularity_list:
#         for typicality_threshold in threshold_list:
#             for user_count in top_users:
#                 for item_count in top_items:
#                     file_name = "Popularity {} Intersection Min {} Threshold {}, Top Items {}, Top Users {}".format(popularity, intersection_min, typicality_threshold, item_count, user_count)
#                     new_file_name = "Merged Clusters " + file_name
#                     cluster_list = get_cluster_list_from_file(file_name)

#                     # merge clusters that are too similar
#                     # print(cluster_list)
#                     cluster_list = merge(cluster_list, 0.75)
#                     # print(cluster_list)


#                     # compute average retweets shared among users in each cluster
#                     compute_cluster_retweet_average(cluster_list, user_to_interaction_count)
                    
#                     save_to_file(new_file_name, cluster_list)




# print table results
# threshold_list = [0.1]
# # threshold_list = [0.5]
# for typicality_threshold in threshold_list:
#     user_to_rir_threshold_filtered, filtered_interaction_count, _ = retweet_dao.user_to_rir_threshold_filtered(user_to_relative_interaction_rate, user_to_interaction_count, typicality_threshold, 5)
#     user_to_rir_top_count_filtered = retweet_dao.user_to_rir_top_count_filtered(user_to_rir_threshold_filtered, filtered_interaction_count, 5)

#     f = open('UserToItems Threshold {}'.format(typicality_threshold), 'w')
#     for user in ['JFutoma', 'david_sontag', 'Yair_Rosenberg', 'propublica', 'random_walker', 'kdphd']:
#         # add interaction count
#         for user_ in user_to_interaction_rate[user]:
#             user_to_interaction_rate[user][user_] = (user_to_interaction_rate[user][user_], user_to_interaction_count[user][user_])

#         for user_ in user_to_rir_threshold_filtered[user]:    
#             user_to_rir_threshold_filtered[user][user_] = (user_to_rir_threshold_filtered[user][user_], filtered_interaction_count[user][user_])
        
#         for user_ in user_to_rir_top_count_filtered[user]:    
#             user_to_rir_top_count_filtered[user][user_] = (user_to_rir_top_count_filtered[user][user_], filtered_interaction_count[user][user_])
        
#         # sort 
#         user_to_interaction_rate[user] = sorted(user_to_interaction_rate[user].items(), key = lambda kv : kv[1][0], reverse=True)
#         user_to_rir_threshold_filtered[user] = sorted(user_to_rir_threshold_filtered[user].items(), key = lambda kv : kv[1][0], reverse=True)
#         user_to_rir_top_count_filtered[user] = sorted(user_to_rir_top_count_filtered[user].items(), key = lambda kv : kv[1][1], reverse=True)

#         f.write("{}\n".format(user))
#         f.write("Table 1(Interaction Users by RIF): {}\n".format(user_to_interaction_rate[user]))
#         f.write("Table 2(Threshold Filtered): {}\n".format(user_to_rir_threshold_filtered[user]))
#         f.write("Table 6(Top 5 Interaction Users by Shared Word Count): {}\n\n".format(user_to_rir_top_count_filtered[user]))



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