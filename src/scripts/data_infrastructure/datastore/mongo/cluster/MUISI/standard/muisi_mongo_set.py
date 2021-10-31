class MUISIMongoSetDAO():
    def __init__(self):
        self.muisi_cluster_collection = None

    def store_clusters(self, clusters, muisi_config):
        self.muisi_cluster_collection.insert_one({
            'clustering_type': "MUISI",
            'intersection_min': muisi_config.intersection_min,
            'popularity': muisi_config.popularity,
            'threshold': muisi_config.threshold,
            'user_count': muisi_config.user_count,
            'item_count': muisi_config.item_count,
            'is_only_popularity': muisi_config.is_only_popularity,
            'clusters': clusters
        })