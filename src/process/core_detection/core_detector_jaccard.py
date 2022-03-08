import enum
import os
import json
from re import I
from src.process.data_cleaning.data_cleaning_distributions import jaccard_similarity
from src.model.user import User
from src.model.local_neighbourhood import LocalNeighbourhood
from typing import Dict
from src.shared.logger_factory import LoggerFactory
import src.clustering_experiments.create_social_graph_and_cluster_local as csgc
from src.clustering_experiments.ranking_users_in_clusters import rank_users

log = LoggerFactory.logger(__name__)

class JaccardCoreDetector():
    """
    Given an initial user, and a "community/topic", determine the core user of
    that community
    """

    def __init__(self, user_getter, user_downloader, user_friends_downloader,
            extended_friends_cleaner,
            local_neighbourhood_downloader,
            local_neighbourhood_tweet_downloader, local_neighbourhood_getter,
            tweet_processor, social_graph_constructor, clusterer, cluster_getter,
            cluster_word_frequency_processor, cluster_word_frequency_getter,
            prod_ranker, con_ranker, ranking_getter, user_tweet_downloader, user_tweet_getter,
                 user_friend_getter):
        self.user_getter = user_getter
        self.user_downloader = user_downloader
        self.user_friends_downloader = user_friends_downloader
        self.user_friend_getter = user_friend_getter
        self.user_tweet_downloader = user_tweet_downloader
        self.user_tweet_getter = user_tweet_getter
        self.extended_friends_cleaner = extended_friends_cleaner
        self.local_neighbourhood_downloader = local_neighbourhood_downloader
        self.local_neighbourhood_tweet_downloader = local_neighbourhood_tweet_downloader
        self.local_neighbourhood_getter = local_neighbourhood_getter
        self.tweet_processor = tweet_processor
        self.social_graph_constructor = social_graph_constructor
        self.clusterer = clusterer
        self.cluster_getter = cluster_getter
        self.cluster_word_frequency_processor = cluster_word_frequency_processor
        self.cluster_word_frequency_getter = cluster_word_frequency_getter
        self.prod_ranker = prod_ranker
        self.con_ranker = con_ranker
        self.ranking_getter = ranking_getter

    def detect_core_by_screen_name(self, screen_name: str, skip_download=False):
        user = self.user_getter.get_user_by_screen_name(screen_name)
        if user is None:
            log.info("Downloading initial user " + str(screen_name))

            self.user_downloader.download_user_by_screen_name(screen_name)
            user = self.user_getter.get_user_by_screen_name(screen_name)

            if user is None:
                msg = "Could not download initial user " + str(screen_name)
                log.error(msg)
                raise Exception(msg)

        log.info("Beginning Core detection algorithm with initial user " + str(screen_name))
        self.detect_core(user.id, skip_download)

    def detect_core(self, initial_user_id: str, skip_download=False):
        log.info("Beginning core detection algorithm for user with id " + str(initial_user_id))

        prev_user_id = str(initial_user_id)
        curr_user_id = None
        top_10_users = []

        # First iteration
        try:
            curr_user_id, top_10_users = self.first_iteration(prev_user_id, skip_download)
        except Exception as e:
            log.exception(e)
            exit()

        # Other iterations
        while str(curr_user_id) != str(prev_user_id):
            prev_user_id = curr_user_id

            try:
                curr_user_id, top_10_users = self.loop_iteration(curr_user_id, top_10_users, skip_download)
            except Exception as e:
                log.exception(e)
                exit()

        log.info("The final user for initial user " + str(initial_user_id) + " is "
                 + self.user_getter.get_user_by_id(str(curr_user_id)).screen_name)
        log.info(f"The top 10 users for the selected cluster in the last iteration were: {top_10_users}")

    def first_iteration(self, user_id: str, skip_download=False):
        if not skip_download:
            self._download(user_id)

        screen_name = self.user_getter.get_user_by_id(user_id).screen_name

        clusters = self._clustering(user_id, 0.2)
        chosen_cluster = self._pick_first_cluster(user_id, clusters)
        self._download_cluster_tweets(chosen_cluster)
        top_10_users = rank_users(screen_name, chosen_cluster)[0]
        curr_user = self.user_getter.get_user_by_screen_name(top_10_users[0])
        curr_user = curr_user.id

        return curr_user, top_10_users

    def _pick_first_cluster(self, user_id, clusters):
        """Returns the largest cluster."""
        # TODO: Figure out a "better" arbitrary solution
        log.info("Picking Default Cluster")
        return clusters[0]

    def loop_iteration(self, user_id: str, curr_top_10_users, skip_download=False):
        if not skip_download:
            self._download(user_id)

        screen_name = self.user_getter.get_user_by_id(user_id).screen_name

        clusters = self._clustering(user_id)
        chosen_cluster = self._select_cluster(user_id, curr_top_10_users, clusters)
        self._download_cluster_tweets(chosen_cluster)
        top_10_users = rank_users(screen_name, chosen_cluster)[0]
        curr_user = self.user_getter.get_user_by_screen_name(top_10_users[0])
        curr_user = curr_user.id

        return curr_user, top_10_users

    def _select_cluster(self, user_id, top_10_users, clusters):
        """Returns the cluster where the sum of the production utilities of the top 10 users of
        the previous iteration is the highest."""
        log.info("Selecting Cluster based on production utilities")

        list_of_prod_values = [0] * len(clusters)
        top_10_users_ids = [self.user_getter.get_user_by_screen_name(top_user).id for top_user in top_10_users]

        for ind, cluster in enumerate(clusters):
            cluster_user_ids = cluster.users
            cluster_user_ids.extend(top_10_users_ids)
            prod_ranker_scores = self.prod_ranker.score_users(cluster_user_ids)

            for top_user_id in top_10_users_ids:
                list_of_prod_values[ind] += prod_ranker_scores[str(top_user_id)]

        ind, val = 0, 0
        for i in range(len(list_of_prod_values)):
            if list_of_prod_values[i] >= val:
                ind = i
                val = list_of_prod_values[i]

        return clusters[ind]

    def _download(self, user_id: str):
            # TODO: Cleaning Friends List by Global and Local Attributes
            user_id = int(user_id)
            screen_name = self.user_getter.get_user_by_id(str(user_id)).screen_name

            log.info(f"Downloading User {screen_name} {user_id}")
            self.user_downloader.download_user_by_id(user_id)

            log.info("Downloading User Tweets")
            self.user_tweet_downloader.download_user_tweets_by_user_id(user_id)

            log.info("Downloading User Friends")
            self.user_friends_downloader.download_friends_users_by_id(user_id)

            log.info("Downloading Local Neighbourhood")
            self.local_neighbourhood_downloader.download_local_neighbourhood_by_id(user_id)

            log.info("Done downloading. Beginning processing")

    def _download_cluster_tweets(self, cluster):
        self.user_tweet_downloader.stream_tweets_by_user_list(cluster.users)

    def _clustering(self, user_id: str, threshold: int=0.3):
        """Returns clusters in descending order of size after refining using jaccard similarity
        (all pairs of users).
        """
        screen_name = self.user_getter.get_user_by_id(user_id).screen_name

        social_graph, local_neighbourhood = csgc.create_social_graph(screen_name)
        refined_social_graph = csgc.refine_social_graph_jaccard_users(screen_name, social_graph, local_neighbourhood, threshold=threshold)
        refined_clusters = csgc.clustering_from_social_graph(screen_name, refined_social_graph)
        sorted_clusters = sorted(refined_clusters, key=lambda c: len(c.users), reverse=True)

        return sorted_clusters
