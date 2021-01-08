from src.model.user import User
from src.shared.utils import cosine_sim
from typing import Dict


class DetectCoreActivity():
    """
    Given an initial user, and a "community/topic", determine the core user of
    that community
    """

    def __init__(self, user_getter, user_downloader, user_friends_downloader,
            local_neighbourhood_downloader,
            local_neighbourhood_tweet_downloader, local_neighbourhood_getter,
            tweet_processor, clusterer, cluster_getter,
            cluster_word_frequency_processor, cluster_word_frequency_getter,
            ranker, ranking_getter):
        self.user_getter = user_getter
        self.user_downloader = user_downloader
        self.user_friends_downloader = user_friends_downloader
        self.local_neighbourhood_downloader = local_neighbourhood_downloader
        self.local_neighbourhood_tweet_downloader = local_neighbourhood_tweet_downloader
        self.local_neighbourhood_getter = local_neighbourhood_getter
        self.tweet_processor = tweet_processor
        self.clusterer = clusterer
        self.cluster_getter = cluster_getter
        self.cluster_word_frequency_processor = cluster_word_frequency_processor
        self.cluster_word_frequency_getter = cluster_word_frequency_getter
        self.ranker = ranker
        self.ranking_getter = ranking_getter

    def detect_core_by_screen_name(self, screen_name: str):
        user = self.user_getter.get_user_by_screen_name(screen_name)
        self.detect_core(user.id)

    def detect_core(self, initial_user_id: str, default_cluster=0):
        prev_users = []
        curr_user_id = initial_user_id

        prev_wf_vectors = []
        curr_wf_vector = None
        while curr_user_id is not in prev_users:
            prev_users.append(curr_user_id)
            if curr_wf_vector is not None:
                prev_wf_vectors.append(curr_wf_vector)

            curr_user_id, curr_wf_vector = loop(curr_user_id,
                prev_wf_vector=curr_wf_vector, default_cluster=0)

            # TODO: Add check for if wf vector is drifting

    def loop(self, user_id: str, prev_wf_vector=None, default_cluster=0, v=False):
        self.user_downloader.download_user_by_id(user_id)
        self.user_friends_downloader.download_friends_users_by_id(user_id)
        self.local_neighbourhood_downloader.download_local_neighbourhood_by_id(user_id)
        self.local_neighbourhood_tweet_downloader.download_user_tweets_by_local_neighbourhood(user_id)

        local_neighbourhood = self.local_neighbourhood_getter.get_local_neighbourhood(user_id)
        self.tweet_processor.process_tweets_by_local_neighbourhood(local_neighbourhood)
        self.clusterer.cluster(user_id)

        clusters, params = self.cluster_getter.get_clusters(user_id)

        curr_cluster = None
        curr_wf_vector = None
        if prev_wf_vector is not None:
            scores = {}
            cluster_wf_vectors = []
            for i in range(len(clusters)):
                self.cluster_word_frequency_processor.compute_cluster_wf_vector(cluster)
                cluster_wf_vector = self.cluster_word_frequency_getter.get_cluster_wf_vector(cluster)
                cluster_wf_vectors.append(cluster_wf_vector)

                scores[i] = cosine_sim(prev_wf_vector, cluster_wf_vector)

            # Sort word frequency vectors by similarity
            sorted = list(sorted(scores, key=scores.get))
            closest_index = sorted[-1]

            curr_cluster = clusters[closest_index]
            curr_wf_vector = cluster_wf_vectors[closest_index]
        else:
            cluster = clusters[default_cluster]
            self.cluster_word_frequency_processor.compute_cluster_wf_vector(cluster)

            curr_cluster = cluster
            curr_wf_vector = self.cluster_word_frequency_getter.get_cluster_wf_vector(cluster)

        self.ranker.rank(cluster)
        ranking = self.ranking_getter.get_ranking(user_id)

        curr_user_id = ranking.get_top_user_id()

        return curr_user_id, curr_wf_vector
