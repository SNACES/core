from pymongo import MongoClient
from collections import Counter
from copy import deepcopy
import datetime
from clustering import *

ds_location = 'mongodb://localhost:27017'
client = MongoClient(ds_location)

# -----------------------------------HELPERS------------------------------------


def detect_all_communities(user_to_items, item_to_users, is_only_popularity):
    cluster_list = []
    count = 0
    # print(len(user_to_items))
    already_seen = []
    for user1 in user_to_items:
        for user2 in user_to_items:
            if user2 not in already_seen and user1 != user2:
                item_intersection = list(set.intersection(
                    set(user_to_items[user1]), set(user_to_items[user2])))

                if item_intersection != []:
                    cluster = detect_single_community(
                        user_to_items, item_to_users, item_intersection, is_only_popularity)
                    if cluster:
                        print(cluster)
                        cluster_list.append(cluster)
                        count += 1
                        # print(count)

            if count == 10:
                return cluster_list

        already_seen.append(user1)

    return cluster_list


def detect_single_community(user_to_items, item_to_users, core_items, is_only_popularity):
    is_converged = False
    num_iterations = 0
    max_iterations = 10  # TODO: hyperparameter

    while not is_converged and num_iterations < max_iterations:
        tmp_core_items = deepcopy(core_items)
        # print(core_users)
        core_users = select(user_to_items, core_items, is_only_popularity)
        core_items = select(item_to_users, core_users, is_only_popularity)
        # print(core_items)
        # print(tmp_core_items)

        if tmp_core_items == core_items:
            is_converged = True

        num_iterations += 1

    return (core_users, core_items) if is_converged else None


def select(user_to_items, core_items, is_only_popularity):
    # compute the popularity of each user wrt the core_items
    user_to_popularity = Counter()
    for user in user_to_items:
        intersect_count = len(set.intersection(
            set(core_items), set(user_to_items[user])))
        user_to_popularity[user] = intersect_count / len(core_items)

    if is_only_popularity:
        # get the top 5 most popular users
        popular_users = [user[0] for user in user_to_popularity.most_common(5)]
        popular_users.sort()
        return popular_users

    # compute the typicality of each user wrt the core_items
    user_to_typicality = Counter()
    for user in user_to_items:
        intersect_count = len(set.intersection(
            set(core_items), set(user_to_items[user])))
        user_to_typicality[user] = intersect_count / len(user_to_items[user])

    # compute the popularity and typicality rankings
    popularity_ranking = {pair[0]: rank
                          for rank, pair in enumerate(user_to_popularity.most_common())}

    typicality_ranking = {pair[0]: rank
                          for rank, pair in enumerate(user_to_typicality.most_common())}

    # compute the overall ranking for each user TODO: is there a bug with this?
    overall_ranking = Counter()
    for user in popularity_ranking:
        overall_ranking[user] = max(
            popularity_ranking[user], typicality_ranking[user])

    # get the top 5 overall ranking for users
    popular_users = [user[0] for user in overall_ranking.most_common()[-6:-1]]
    # popular_users = [user[0] for user in overall_ranking.most_common(5)]
    # for user in popular_users:
    # print(overall_ranking[user])
    popular_users.sort()
    return popular_users


# -------------------------------User Tweets------------------------------------
# get user_to_items from database
word_freq_db = client['WordFreq-Test2']
user_word_freq_collection = word_freq_db['UserRelativeWordFreq']
user_to_items = {}
for doc in user_word_freq_collection.find():
    user = doc['User']
    modified_wf_vector = Counter(doc['RelativeWordFrequency'])
    words_not_in_wf_vector = doc['UserWordsNotInGlobal']

    # compute modified user relative wf
    if modified_wf_vector != {}:  # TODO: careful about this corner case
        max_value = modified_wf_vector[max(modified_wf_vector)]
        for word in words_not_in_wf_vector:
            modified_wf_vector[word] = 10 * max_value
        # get 50 of the most common words
        final_wf_vector = Counter()
        for item in modified_wf_vector.most_common(50):
            final_wf_vector[item[0]] = item[1]

        user_to_items[user] = final_wf_vector


# # compute item_to_users and store to database
# item_to_users = {}
# for user in user_to_items:
#     for item in user_to_items[user]:
#         if item not in item_to_users:
#             item_to_users[item] = []
#         item_to_users[item].append(user)

# # call detect all communities
# clusters = detect_all_communities(user_to_items, item_to_users, False)


# # save results
# word_freq_db = client['WordFreqClustering1']

# user_tweets_popularity_only = word_freq_db['UserTweetsOnlyPopularity']
# for cluster in clusters:
#     user_tweets_popularity_only.insert_one({
#         'Users': cluster[0],
#         'Items': cluster[1]
#     })

# user_tweets_popularity_and_typicality = word_freq_db['UserTweetsPopularityTypicality']
# for cluster in clusters:
#     user_tweets_popularity_and_typicality.insert_one({
#         'Users': cluster[0],
#         'Items': cluster[1]
#     })


# ----------------------------------Retweets-------------------------------------
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


# ------------------------------------------------------------------------------
# Use cluster relative word frequency to get most typical words for

# clusters from user to words(popularity)
most_common_clusters = [["OsitaNwanevu", "aselbst", "ewarren", "ezraklein", "julia_azari"],
                        ["JFutoma", "catherineols", "logangraham",
                            "ndiakopoulos", "yisongyue"],
                        ["TrooperSanders", "aselbst", "gokstudio",
                            "hima_lakkaraju", "kongaloosh"],
                        ["JFutoma", "fhuszar", "gokstudio",
                            "logangraham", "tdietterich"],
                        ["JFutoma", "aselbst", "math_rachel",
                            "packer_ben", "yisongyue"],
                        ["AidanNGomez", "berty38", "hima_lakkaraju",
                            "irenetrampoline", "tw_killian"]
                        ]
result = get_clusters_most_common_words(most_common_clusters, user_to_items)
print(result)


# clusters from user to retweets(popularity)
most_common_clusters = [['JFutoma', 'SmithaMilli', 'YBenkler', 'aselbst', 'karen_ec_levy'],
                        ['JFutoma', 'SmithaMilli', 'YBenkler', 'agstrait', 'karen_ec_levy']]
result = get_clusters_most_common_words(most_common_clusters, user_to_items)
print(result)

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
