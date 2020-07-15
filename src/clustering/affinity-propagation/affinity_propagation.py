from pymongo import MongoClient
from collections import Counter
from sklearn.cluster import AffinityPropagation
import numpy as np
from clustering import *

ds_location = 'mongodb://localhost:27017'
client = MongoClient(ds_location)

# get user relative wf from database, then compute modified version, where
# "not in" words are added and are assigned to 10x the max relative wf for each wf vector
word_freq_db = client['WordFreq-Test2']
user_word_freq_collection = word_freq_db['UserRelativeWordFreq']
user_word_freq = {}
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

        user_word_freq[user] = final_wf_vector


# get clusters
clusters = get_clusters(user_word_freq)

# get the 5 largest clusters
most_common_clusters = []
for i in range(5):
    common_cluster = max(clusters, key=len)
    clusters.remove(common_cluster)
    most_common_clusters.append(common_cluster)
# print(most_common_clusters)
# print(len(most_common_clusters))

# calculate the cluster relative wf
cluster_rwf_list = []
for cluster in most_common_clusters:
    cluster_rwf_list.append(
        cluster_relative_frequency(user_word_freq, cluster))
# print(len(cluster_rwf_list))

# for each of the 5 cluster relative wf, get the top 20 words
cluster_most_common_words = []
for cluster_rwf in cluster_rwf_list:
    most_common_words = []
    for item in cluster_rwf.most_common(20):
        most_common_words.append(item[0])
    cluster_most_common_words.append(most_common_words)
    # print(len(most_common_words))
# print(cluster_most_common_words)

cluster_overlap_info = []
for i in range(5):
    for j in range(5):
        if i < j:
            cluster_overlap_info.append("({}, {}) Word Overlap: {} Min Num Words: {}".format(i, j,
                                                                                        word_overlap(
                                                                                            cluster_rwf_list[i], cluster_rwf_list[j]),
                                                                                        min(len(cluster_rwf_list[i]), len(cluster_rwf_list[j]))))

# store results and intermediates in database
clustering_experiment = client['WordFreqClustering1']
user_word_freq_collection = clustering_experiment['ClusteringResultsWordOverlap']
user_word_freq_collection.insert_one({
        "Clusters": most_common_clusters,
        "ClusterRelativeWF": cluster_rwf_list,
        "ClusterMostCommonWords": cluster_most_common_words,
        "ClusterWordOverlapInfo": cluster_overlap_info
})
