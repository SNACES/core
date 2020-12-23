
class Clusterer():
    def __init__(self, social_graph_getter, cluster_setter):
        self.social_graph_getter = social_graph_getter
        self.cluster_setter = cluster_setter

    def cluster(self, params):
        raise NotImplementedError("Subclasses should implement this")
