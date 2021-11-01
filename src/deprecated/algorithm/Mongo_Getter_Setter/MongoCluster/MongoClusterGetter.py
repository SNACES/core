class MongoClusterGetter():
    def __init__(self):
        self.collection = None

    def set_collection(self, collection) -> None:
        self.collection = collection

    def get_clusters(self, cluster_num: int, base_user:str, clustering_type: str, params=None):
        all_clusters = None
        if params is None:
            all_clusters = self.collection.find({}, {'clustering_type': 1, "base_user":1, "clusters":1})
        else:
            all_clusters = self.collection.find({}, {'clustering_type': 1, "base_user":1, "clusters":1, params: 1})

        clustering_list = []
        for item in all_clusters:
            if item["clustering_type"] == clustering_type and item["base_user"] == base_user:
                clustering_list = item["clusters"] 
        clustering_list = self.rank_cluster_by_length(clustering_list)
        target_cluster = clustering_list[cluster_num]

        return target_cluster

    def rank_cluster_by_length(self, all_clusters):
        all_clusters = sorted(all_clusters, key = lambda x: len(x), reverse = True)
        return all_clusters
        