from src.model.social_graph.social_graph import SocialGraph


class SocialGraphSetter():
    def store_social_graph(self, social_graph: SocialGraph):
        raise NotImplementedError("Subclasses should implement this")
