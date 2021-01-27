from src.model.user import User
from typing import Dict


class CoreDetector():
    """
    Given an initial user, and a "community/topic", determine the core user of
    that community
    """

    def __init__(self, user_getter, user_downloader, user_friends_downloader,
            local_neighbourhood_downloader,
            local_neighbourhood_tweet_downloader, local_neighbourhood_getter,
            tweet_processor, social_graph_constructor, clusterer, cluster_getter,
            cluster_word_frequency_processor, cluster_word_frequency_getter,
            ranker, ranking_getter):
        self.user_getter = user_getter
        self.user_downloader = user_downloader
        self.user_friends_downloader = user_friends_downloader
        self.local_neighbourhood_downloader = local_neighbourhood_downloader
        self.local_neighbourhood_tweet_downloader = local_neighbourhood_tweet_downloader
        self.local_neighbourhood_getter = local_neighbourhood_getter
        self.tweet_processor = tweet_processor
        self.social_graph_constructor = social_graph_constructor
        self.clusterer = clusterer
        self.cluster_getter = cluster_getter
        self.cluster_word_frequency_processor = cluster_word_frequency_processor
        self.cluster_word_frequency_getter = cluster_word_frequency_getter
        self.ranker = ranker
        self.ranking_getter = ranking_getter

    def detect_core_by_screen_name(self, screen_name: str):
        # TODO add a catch statement that downloads the user if the getter returns None
        user = self.user_getter.get_user_by_screen_name(screen_name)
        self.detect_core(user.id)

    def detect_core(self, initial_user_id: str, default_cluster=0):
        prev_users = []
        curr_user_id = initial_user_id

        prev_wf_vectors = []
        curr_wf_vector = None
        while curr_user_id not in prev_users:
            prev_users.append(str(curr_user_id))
            if curr_wf_vector is not None:
                prev_wf_vectors.append(curr_wf_vector)

            curr_user_id, curr_wf_vector = self.loop(curr_user_id,
                prev_wf_vector=curr_wf_vector, default_cluster=0)

            # TODO: Add check for if wf vector is drifting

    def loop(self, user_id: str, prev_wf_vector=None, default_cluster=0, v=True):
        # TODO Add flag for skipping download step
        if v:
            print("Downloading User")
        self.user_downloader.download_user_by_id(user_id)
        if v:
            print("Downloading User Friends")
        self.user_friends_downloader.download_friends_users_by_id(user_id)
        if v:
            print("Downloading Local Neighbourhood")
        self.local_neighbourhood_downloader.download_local_neighbourhood_by_id(user_id)
        if v:
            print("Downloading Local Neighbourhood Tweets")
        self.local_neighbourhood_tweet_downloader.download_user_tweets_by_local_neighbourhood(user_id)
        if v:
            print("Done downloading Beginning Processing")

        local_neighbourhood = self.local_neighbourhood_getter.get_local_neighbourhood(user_id)
        if v:
            print("Processing Local Neighbourhood Tweets")
        self.tweet_processor.process_tweets_by_local_neighbourhood(local_neighbourhood)

        if v:
            print("Construct social graph")
        self.social_graph_constructor.construct_social_graph_from_local_neighbourhood(user_id)

        if v:
            print("Clustering")
        self.clusterer.cluster(user_id, {})
        clusters, params = self.cluster_getter.get_clusters(user_id)

        curr_cluster = None
        curr_wf_vector = None
        if prev_wf_vector is not None:
            if v:
                print("Picking Cluster")

            scores = {}
            cluster_wf_vectors = []
            for i in range(len(clusters)):
                cluster = clusters[i]

                self.cluster_word_frequency_processor.process_cluster_word_frequency_vector(cluster.users)
                cluster_wf_vector = self.cluster_word_frequency_getter.get_cluster_word_frequency_by_ids(cluster.users)
                cluster_wf_vectors.append(cluster_wf_vector)

                scores[i] = cluster_wf_vector.word_frequency_vector.cosine_sim_to(prev_wf_vector.word_frequency_vector)

            # Sort word frequency vectors by similarity
            sorted_wf_vectors = list(sorted(scores, key=scores.get, reverse=True))
            closest_index = sorted_wf_vectors[0]

            curr_cluster = clusters[closest_index]
            curr_wf_vector = cluster_wf_vectors[closest_index]
        else:
            if v:
                print("Picking Default Cluster")
            cluster = clusters[default_cluster]
            self.cluster_word_frequency_processor.process_cluster_word_frequency_vector(cluster.users)

            curr_cluster = cluster
            curr_wf_vector = self.cluster_word_frequency_getter.get_cluster_word_frequency_by_ids(cluster.users)

        if v:
            print("Ranking Cluster")
        self.ranker.rank(user_id, params)
        ranking = self.ranking_getter.get_ranking(user_id)

        curr_user_id = ranking.get_top_user_id()

        if v:
            print("Highest Ranking User is " + str(curr_user_id))

        return curr_user_id, curr_wf_vector
