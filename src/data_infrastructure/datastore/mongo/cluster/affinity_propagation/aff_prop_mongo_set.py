class AffinityPropagationMongoSetDAO():
    def __init__(self):
        self.clusters_collection = None

    def store_clusters(self, cluster_list, cluster_rwf_list, cluster_most_common_words):
        self.clusters_collection.insert_one({
            'clustering_type': "Affinity Propagation",
            'clusters': cluster_list,
            'cluster_rwf': cluster_rwf_list,
            'cluster_most_common_words': cluster_most_common_words,
        })
    
