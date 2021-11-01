# TODO:
class LabelPropagationMongoGetDAO:
    def __init__(self):
        self.clusters_collection = None

    def get_clusters(self):
        clusters_list = self.clusters_collection.find()
        return clusters_list