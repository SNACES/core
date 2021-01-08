from typing import List

class CountConnect():
    def __init__(self, cluster_getter, user_friends):
        self.cluster_getter = cluster_getter
        self.user_friends_getter = user_friends
    
    def count_connect_between_cluster(self, cluster_num_1, cluster_num_2, base_user, cluster_type):
        cluster_1 = self.cluster_getter.get_clusters(cluster_num_1, base_user, cluster_type)
        cluster_2 = self.cluster_getter.get_clusters(cluster_num_2, base_user, cluster_type)
        _, all_dict = self.user_friends_getter.get_user_neighbourhood(base_user)

        dict_1 = {}
        dict_2 = {}

        for users in all_dict:
            if users in cluster_1:
                dict_1[users] = all_dict[users]
            elif users in cluster_2:
                dict_2[users] = all_dict[users]
            
        connect1 = self.connectivity(dict_1, dict_1)
        connect2 = self.connectivity(dict_2, dict_2)
        connect12 = self.connectivity(dict_1, dict_2)

        print("connectedness in cluster 1 is: ", connect1)
        print("connectedness in cluster 2 is: ", connect2)
        print("connectedness between cluster 1 and 2 is: ", connect12)
            
    def connectivity(self, dict1, dict2):
        result = 0
        for user1 in dict1:
            for user2 in dict2:
                if user2 in dict1[user1]:
                    result +=1
        return result  

