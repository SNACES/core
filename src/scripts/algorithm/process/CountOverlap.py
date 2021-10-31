class CountOverlap():
    def __init__(self, cluster_getter, user_friends):
        self.cluster_getter = cluster_getter
        self.user_friends_getter = user_friends
    
    def count_overlap_between_cluster(self, cluster_num_1, cluster_num_2, base_user, cluster_type_1, cluster_type_2):
        cluster_1 = self.cluster_getter.get_clusters(cluster_num_1, base_user, cluster_type_1)
        cluster_2 = self.cluster_getter.get_clusters(cluster_num_2, base_user, cluster_type_2)

        overlap_num = 0
        for users in cluster_1:
            if users in cluster_2:
                overlap_num += 1
        print("cluster 1 has number of users: ", len(cluster_1))
        print("cluster 2 has number of users: ", len(cluster_2))
        print("overlap users number is: ", overlap_num)
            
