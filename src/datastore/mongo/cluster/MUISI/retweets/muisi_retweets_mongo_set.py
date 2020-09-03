class MUISIRetweetsMongoSetDAO():
    def __init__(self):
        self.muisi_retweets_cluster_collection = None

    def store_clusters(self, clusters, muisi_retweet_config):
        self.muisi_retweets_cluster_collection.insert_one({
            'clustering_type': "MUISI with Retweets",
            'intersection_min': muisi_retweet_config.intersection_min,
            'popularity': muisi_retweet_config.popularity,
            'user_count': muisi_retweet_config.user_count,
            'clusters': muisi_retweet_config.clusters
        })