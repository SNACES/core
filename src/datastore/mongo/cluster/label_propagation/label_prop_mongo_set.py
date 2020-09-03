class LabelPropagationMongoSetDAO():
    def __init__(self):
        self.clusters_collection = None

    def store_clusters(self, user, cluster_list):
        self.clusters_collection.insert_one({
            'clustering_type': "Label Propagation",
            'base_user': user,
            'clusters': cluster_list
        })