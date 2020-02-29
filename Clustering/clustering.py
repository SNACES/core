from pymongo import MongoClient
from collections import Counter
from sklearn.cluster import AffinityPropagation
import numpy as np

def cluster_relative_frequency(user_to_rwf, cluster) -> Counter:
    rwf_list = []
    for user in user_to_rwf:
        if user in cluster:
            rwf_list.append(user_to_rwf[user])

    return sum(rwf_list, Counter())


def get_fitted_affinity(user_to_rwf, distance):
    aff_prop = AffinityPropagation(affinity='precomputed')

    similarity_mtx = np.zeros((len(user_to_rwf), len(user_to_rwf)))
    if distance == 'cosine':
        i = 0
        for user1 in user_to_rwf:
            j = 0
            for user2 in user_to_rwf:
                similarity_mtx[i][j] = cosine_sim(
                    user_to_rwf[user1], user_to_rwf[user2])
                j += 1
            i += 1
    else:
        i = 0
        for user1 in user_to_rwf:
            j = 0
            for user2 in user_to_rwf:
                similarity_mtx[i][j] = word_overlap(
                    user_to_rwf[user1], user_to_rwf[user2])
                j += 1
            i += 1

    median = np.median(similarity_mtx)

    for i in range(len(user_to_rwf)):
        similarity_mtx[i][i] = median

    return aff_prop.fit(similarity_mtx)


def get_clusters(user_to_rwf):
    """Gets a list containing clusters of users."""
    fitted = get_fitted_affinity(user_to_rwf, 'cosine')
    d = {}
    li = fitted.labels_
    for i in range(len(li)):
        if li[i] not in d.keys():
            d[li[i]] = [list(user_to_rwf.keys())[i]]
        else:
            d[li[i]].append(list(user_to_rwf.keys())[i])

    return list(d.values())


def cosine_sim(counter1, counter2):
    """An implementation of cosine similarity based on word counters rather than vectors"""
    norm_c1 = sum([x**2 for x in counter1.values()])**0.5
    norm_c2 = sum([x**2 for x in counter2.values()])**0.5
    dot_product = 0
    for key in set.intersection(set(counter1.keys()), set(counter2.keys())):
        dot_product += counter1[key]*counter2[key]

    return dot_product/(norm_c1*norm_c2) if norm_c1 != 0 and norm_c2 != 0 else -1


def word_overlap(counter1, counter2):
    """Find the number of overlapping words between two counters"""
    set1 = set(counter1.keys())
    set2 = set(counter2.keys())
    return len(set.intersection(set1, set2))



def get_clusters_most_common_words(most_common_clusters, user_word_freq):
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
    return cluster_most_common_words