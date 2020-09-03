import numpy as np

from pymongo import MongoClient
from collections import Counter
from sklearn.cluster import AffinityPropagation as AP
from src.shared.lib import cosine_sim, word_overlap
from src.process.clustering.clustering_lib import *

class AffinityPropagation():
    def gen_clusters(self, word_freq_getter, aff_prop_setter):
        user_to_rwf = word_freq_getter.get_relative_user_word_frequency_vector()
        cluster_list = self.get_clusters(user_to_rwf)
        cluster_rwf_list = [cluster_relative_frequency(user_to_rwf, cluster)
                            for cluster in cluster_list]
        cluster_most_common_words = get_clusters_most_common_words(cluster_list, cluster_rwf_list)
        aff_prop_setter.store_clusters(cluster_list, cluster_rwf_list, cluster_most_common_words)

        return cluster_list, cluster_rwf_list, cluster_most_common_words

    def get_clusters(self, user_to_rwf):
        """Gets a list containing clusters of users."""
        fitted = self.get_fitted_affinity(user_to_rwf, 'cosine')
        d = {}
        li = fitted.labels_
        for i in range(len(li)):
            if li[i] not in d.keys():
                d[li[i]] = [list(user_to_rwf.keys())[i]]
            else:
                d[li[i]].append(list(user_to_rwf.keys())[i])

        return list(d.values())

    def get_fitted_affinity(self, user_to_rwf, distance):
        aff_prop = AP(affinity='precomputed')

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



