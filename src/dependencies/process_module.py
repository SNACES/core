from src.dependencies.dao_module import DAOModule


class ProcessModule():
    """
    The process module is used to abstract the creation of processes, so they
    can be injected into classes which depend on them
    """

    def __init__(self, dao_module: DAOModule):
        self.dao_module = dao_module

    # Clustering
    def get_clusterer(self):
        social_graph_getter = self.dao_module.get_social_graph_getter()
        cluster_setter = self.dao_module.set_social_graph_setter()

        return Clusterer(social_graph_getter, cluster_setter)

    # Download
    def get_follower_downloader(self):
        pass

    def get_friend_downloader(self):
        pass

    def get_local_neighbourhood_downloader(self):
        pass

    def get_local_neighbourhood_tweet_downloader(self):
        pass

    def get_tweet_downloader(self):
        pass

    def get_twitter_downloader(self):
        pass

    def get_user_downloader(self):
        pass

    def get_user_tweet_downloader(self):
        pass

    # Ranking TODO: Update to use ranker factory
    def get_followers_ranker(self):
        pass

    def get_retweets_ranker(self):
        pass

    # Processing
    def tweet_processor(self):
        pass

    # Social Graph
    def get_social_graph_constructor(self):
        pass
