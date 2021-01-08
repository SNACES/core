from src.dependencies.dao_module import DAOModule
from src.dependencies.process_module import ProcessModule
from src.activity.detect_core_activity import DetectCoreActivity


class ActivityModule():
    def __init__(self, dao_module, process_module):
        self.dao_module = dao_module
        self.process_module = process_module

    def get_detect_core_activity(self):
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

        return DetectCoreActivity(user_getter, user_downloader,
            user_friends_downloader, local_neighbourhood_downloader,
            local_neighbourhood_tweet_downloader, local_neighbourhood_getter,
            tweet_processor, clusterer, cluster_getter,
            cluster_word_frequency_processor, cluster_word_frequency_getter,
            ranker, ranking_getter)
