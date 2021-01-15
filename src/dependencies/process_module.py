from src.dependencies.dao_module import DAOModule
from src.process.clustering.clusterer_factory import ClustererFactory
from src.process.download.user_downloader import TwitterUserDownloader
from src.process.raw_tweet_processing.tweet_processor import TweetProcessor
from src.process.user_word_frequency.user_word_frequency_processor import UserWordFrequencyProcessor


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

        return ClustererFactory.create_clusterer("label_propogation",
            [social_graph_getter, cluster_setter])

    # Core Detection
    def get_core_detector(self):
        user_getter = self.dao_module.get_user_getter()
        user_downloader = self.process_module.get_user_downloader()
        user_friends_downloader = self.process_module.get_user_friends_downloader()
        local_neighbourhood_downloader = self.process_module.get_local_neighbourhood_downloader()
        local_neighbourhood_tweet_downloader = self.process_module.get_local_neighbourhood_tweet_downloader()
        local_neighbourhood_getter = self.dao_module.get_local_neighbourhood_getter()
        tweet_processor = self.process_module.get_tweet_processor()
        clusterer = self.process_module.get_clusterer()
        cluster_getter = self.dao_module.get_cluster_getter()
        cluster_word_frequency_processor = self.process_module.get_cluster_word_frequency_processor()
        cluster_word_frequency_getter = self.dao_module.get_cluster_word_frequency_getter()
        ranker = self.process_module.get_ranker()
        ranking_getter = self.dao_module.get_ranking_getter()

        return CoreDetector(user_getter, user_downloader,
            user_friends_downloader, local_neighbourhood_downloader,
            local_neighbourhood_tweet_downloader, local_neighbourhood_getter,
            tweet_processor, clusterer, cluster_getter,
            cluster_word_frequency_processor, cluster_word_frequency_getter,
            ranker, ranking_getter)

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
        twitter_getter = self.dao_module.get_twitter_getter()
        user_setter = self.dao_module.get_user_setter()

        user_downloader = TwitterUserDownloader(twitter_getter, user_setter)
        return user_downloader

    def get_user_tweet_downloader(self):
        pass

    # Ranking TODO: Update to use ranker factory
    def get_followers_ranker(self):
        pass

    def get_retweets_ranker(self):
        pass

    # Processing
    def get_tweet_processor(self):
        raw_tweet_getter = self.dao_module.get_user_tweet_getter()
        processed_tweet_setter = self.dao_module.get_processed_tweet_setter()

        tweet_processor = TweetProcessor(raw_tweet_getter, processed_tweet_setter)
        return tweet_processor

    # Social Graph
    def get_social_graph_constructor(self):
        pass


    
    # User Word Frequency
    def get_user_word_frequency_processor(self):
        processed_tweet_getter = self.dao_module.get_processed_tweet_getter()
        user_word_frequency_getter = self.dao_module.get_user_word_frequency_getter()
        user_word_frequency_setter = self.dao_module.get_user_word_frequency_setter()
        global_word_frequency_getter = self.dao_module.get_global_word_frequency_getter()
        
        user_word_frequency_processor = UserWordFrequencyProcessor(processed_tweet_getter, user_word_frequency_getter, 
                                        user_word_frequency_setter, global_word_frequency_getter)
        return user_word_frequency_processor
