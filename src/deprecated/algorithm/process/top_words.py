from typing import List
from collections import Counter

class TopWords():
    def __init__(self, cluster_getter, wordfrequency_getter, top_words_setter):
        self.cluster_getter = cluster_getter
        self.wordfrequency_getter = wordfrequency_getter
        self.top_words_setter = top_words_setter
    
    def find_top_words(self, cluster_num, base_user, cluster_type):
        cluster_list = self.cluster_getter.get_clusters(cluster_num, base_user, cluster_type)
        user_to_rwf = self.wordfrequency_getter.get_relative_word_frequency(cluster_num, base_user, cluster_type)

        cluster_rwf_list = self.cluster_relative_frequency(user_to_rwf, cluster_list)
        top_100_words = []
        for item in cluster_rwf_list.most_common(100):
            top_100_words.append(item[0])
        print("the top 100 words are:", top_100_words)
        
        self.top_words_setter.set_top_words(cluster_num, base_user, cluster_type, top_100_words)

    def cluster_relative_frequency(self, user_to_rwf, cluster) -> Counter:
        rwf_list = []
        for user in user_to_rwf:
            if user in cluster:
                rwf_list.append(Counter(user_to_rwf[user]))

        return sum(rwf_list, Counter())



