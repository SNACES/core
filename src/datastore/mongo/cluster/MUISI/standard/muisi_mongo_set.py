class MUISIMongoSetDAO():
    def __init__(self):
        self.muisi_cluster_collection = None

    def store_clusters(self, clusters, intersection_min, popularity, threshold, 
                       user_count, item_count, is_only_popularity):
        self.muisi_cluster_collection.insert_one({
            'clustering_type': "MUISI",
            'intersection_min': intersection_min,
            'popularity': popularity,
            'threshold': threshold,
            'user_count': user_count,
            'item_count': item_count,
            'is_only_popularity': is_only_popularity,
            'clusters': clusters
        })