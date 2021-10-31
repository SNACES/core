from typing import List
from collections import Counter

class TopUsers():
    def __init__(self, cluster_getter, wordfrequency_getter, topwords_getter, top_users_setter):
        self.cluster_getter = cluster_getter
        self.wordfrequency_getter = wordfrequency_getter
        self.topwords_getter = topwords_getter
        self.top_users_setter = top_users_setter
    
    def find_top_users(self, cluster_num, base_user, cluster_type):
        cluster_list = self.cluster_getter.get_clusters(cluster_num, base_user, cluster_type)
        user_to_rwf = self.wordfrequency_getter.get_relative_word_frequency(cluster_num, base_user, cluster_type)
        top_words = self.topwords_getter.get_top_words(cluster_num, base_user, cluster_type)

        users_num = len(cluster_list)
        proportion_dict = {}

        result = {}
        for user in cluster_list:
            if user in user_to_rwf:
                user_wfs = user_to_rwf[user]
                appear_num = 0
                for words in top_words:
                    if words not in proportion_dict:
                        proportion_dict[words] = 0
                    if words in user_wfs:
                        proportion_dict[words] += 1
                        appear_num += user_wfs[words]
                result[user] = appear_num
                #print(appear_num)
                #print(user)
            else:
                result[user] = 0

        print("appear proportion is: ", proportion_dict)

        user_to_words = []
        for users in result:
            user_to_words.append(result[users])

        five_top = sorted( [(x,i) for (i,x) in enumerate(user_to_words)], reverse=True )[:5]

        top_index = []
        for index in five_top:
            top_index.append(index[1])

        top_five_users = []
        for idex in top_index:
            top_five_users.append(list(result.keys())[idex])
        print("top five users: ", top_five_users)

        top_words_with_threshold = []
        for words in proportion_dict:
            if proportion_dict[words] > users_num / 10 and proportion_dict[words] > 1:
                top_words_with_threshold.append((words, proportion_dict[words]))
        print("top words with threshold: ", top_words_with_threshold)

        self.top_users_setter.set_top_users(cluster_num, base_user, cluster_type, top_five_users)

