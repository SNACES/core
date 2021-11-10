import os
import json

from src.process.core_detection.boxplot_generator import generate_boxplot, \
    generate_hist, generate_scatterplot
from src.process.core_detection.scatter_plot_generator import generate_plot, \
    generate_plot_2
from src.process.data_cleaning.data_cleaning_distributions import jaccard_similarity
from src.model.local_neighbourhood import LocalNeighbourhood
from src.shared.logger_factory import LoggerFactory

log = LoggerFactory.logger(__name__)

class CoreDetector():
    """
    Given an initial user, and a "community/topic", determine the core user of
    that community
    """

    def __init__(self, user_getter, user_downloader, user_friends_downloader,
                 extended_friends_cleaner, local_neighbourhood_downloader,
                 local_neighbourhood_tweet_downloader,
                 local_neighbourhood_getter,
                 tweet_processor, social_graph_constructor, clusterer,
                 cluster_getter, cluster_word_frequency_processor,
                 cluster_word_frequency_getter, prod_ranker, con_ranker,
                 ranking_getter, user_tweet_downloader, user_tweet_getter,
                 user_liked_tweet_getter,
                 user_friend_getter, like_prod_ranker, like_con_ranker):
        self.user_getter = user_getter
        self.user_downloader = user_downloader
        self.user_friends_downloader = user_friends_downloader
        self.user_friend_getter = user_friend_getter
        self.user_tweet_downloader = user_tweet_downloader
        self.user_tweet_getter = user_tweet_getter
        self.user_liked_tweet_getter = user_liked_tweet_getter
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
        self.like_prod_ranker = like_prod_ranker
        self.like_con_ranker = like_con_ranker

    def detect_core_by_screen_name(self, screen_name: str):
        user = self.user_getter.get_user_by_screen_name(screen_name)
        if user is None:
            log.info("Downloading initial user " + str(screen_name))

            self.user_downloader.download_user_by_screen_name(screen_name)
            user = self.user_getter.get_user_by_screen_name(screen_name)

            if user is None:
                msg = "Could not download initial user " + str(screen_name)
                log.error(msg)
                raise Error(msg)

        log.info("Beginning Core detection algorithm with initial user " + str(screen_name))
        self.detect_core(user.id)

    def detect_core(self, initial_user_id: str, default_cluster=1):
        log.info("Beginning core detection algorithm for user with id " + str(initial_user_id))

        # prev_users = []
        curr_user_id = initial_user_id
        prev_user_id = None
        prev_wf_vectors = []
        curr_wf_vector = None
        prev_cluster = None
        count = 0
        while str(curr_user_id) != str(prev_user_id):

            prev_user_id = curr_user_id
            if curr_wf_vector is not None:
                prev_wf_vectors.append(curr_wf_vector)

            try:
                curr_user_id, curr_wf_vector, curr_cluster = self.loop(int(curr_user_id), count, prev_cluster,
                    prev_wf_vector=curr_wf_vector, default_cluster=default_cluster)
                prev_cluster = curr_cluster
                count += 1
            except Exception as e:
                log.exception(e)
                exit()

        log.info("The final user for initial user " + str(initial_user_id) + " is "
                 + self.user_getter.get_user_by_id(str(curr_user_id)).screen_name)


            # TODO: Add check for if wf vector is drifting

    def loop(self, user_id: str, count, prev_cluster, prev_wf_vector=None, default_cluster=1, v=True, skip_download=True):
        # downloaded_users = ["876274407995527169", "985158406125375488", "359831209"]
        downloaded_users = []
        if not skip_download or str(user_id) not in downloaded_users:
            # TODO Add flag for skipping download step
            log.info("Downloading User")
            self.user_downloader.download_user_by_id(user_id)

            log.info("Downloading User Tweets")
            self.user_tweet_downloader.download_user_tweets_by_user_id(str(user_id))

            log.info("Downloading User Friends")
            self.user_friends_downloader.download_friends_users_by_id(user_id)

            log.info("Cleaning Friends List by Global Attributes")
            user = self.user_getter.get_user_by_id(str(user_id))
            follower_thresh = 0.1 * user.followers_count
            friend_thresh = 0.1 * user.friends_count
            tweet_thresh = 0.1 * len(self.user_tweet_getter.get_tweets_by_user_id_time_restricted(str(user_id)))
            clean_list = self.extended_friends_cleaner.clean_friends_global(user_id,
                            tweet_threshold=tweet_thresh, follower_threshold=follower_thresh, friend_threshold=friend_thresh)

            log.info("Downloading Local Neighbourhood")
            self.local_neighbourhood_downloader.download_local_neighbourhood_by_id(user_id)

            log.info("Cleaning Friends List by Local Attributes")
            self.extended_friends_cleaner.clean_friends_local(user_id, clean_list)

            log.info("Updating Local Neighbourhood")
            self.local_neighbourhood_downloader.download_local_neighbourhood_by_id(user_id)

            # log.info("Downloading Local Neighbourhood Tweets")
            # self.local_neighbourhood_tweet_downloader.download_user_tweets_by_local_neighbourhood(user_id)

        log.info("Done downloading Beginning Processing")
        local_neighbourhood = self.local_neighbourhood_getter.get_local_neighbourhood(user_id)

        # Refined Friends Method
        log.info("Refining Friends List:")
        user_list = local_neighbourhood.get_user_id_list()
        friends_map = {}
        for user in user_list:
            friends_list = []
            friends = local_neighbourhood.get_user_friends(user)

            # print(len(friends))
            for friend in friends:
                if user in local_neighbourhood.get_user_friends(str(friend)):
                    friends_list.append(friend)
                if user == str(user_id):
                    if int(user) in self.user_friend_getter.get_user_friends_ids(str(friend)):
                        friends_list.append(friend)
            # print(len(friends_list))
            friends_map[user] = friends_list

        log.info("Refining by Jaccard Similarity:")
        for user in user_list:
            friends_list = friends_map[user]
            similarities = {}
            for friend in friends_list:
                sim = jaccard_similarity(friends_list, friends_map[str(friend)])
                similarities[friend] = sim
            sorted_users = sorted(similarities, key=similarities.get, reverse=True)
            top_sum = 0
            for top_user in sorted_users[:10]:
                top_sum += similarities[top_user]
            if len(sorted_users) >= 10:
                thresh = 0.1 * (top_sum / 10)
            elif len(sorted_users) == 0:
                thresh = 0
            else:
                thresh = 0.1 * (top_sum / len(sorted_users))
            # Can do more efficiently using binary search
            index = len(sorted_users)
            for i in range(len(sorted_users)):
                user = sorted_users[i]
                if similarities[user] < thresh:
                    index = i
                    break
            friends_map[user] = sorted_users[:index]

        log.info("Setting Local Neighborhood:")
        refined_local_neighborhood = LocalNeighbourhood(str(user_id), None, friends_map)
        social_graph = self.social_graph_constructor.construct_social_graph_from_local_neighbourhood(user_id, refined_local_neighborhood)
        log.info("Clustering:")
        clusters = self.clusterer.cluster_by_social_graph(user_id, social_graph, None)

        # log.info("Processing Local Neighbourhood Tweets")
        # self.tweet_processor.process_tweets_by_local_neighbourhood(local_neighbourhood)

        # log.info("Construct social graph")
        # self.social_graph_constructor.construct_social_graph(user_id)
        #
        # log.info("Performing Clustering")
        # self.clusterer.cluster(user_id, {"graph_type": "union"})
        # #self.clusterer.cluster_by_social_graph(user_id, social_graph, {"graph_type": "union"})
        # clusters, params = self.cluster_getter.get_clusters(user_id, params={"graph_type": "union"})

        curr_wf_vector = None

        # Cluster chosen using word vector similarity
        # if prev_wf_vector is not None:
        #     log.info("Picking Cluster")
        #
        #     scores = {}
        #     cluster_wf_vectors = []
        #     for i in range(len(clusters)):
        #         cluster = clusters[i]
        #
        #         self.cluster_word_frequency_processor.process_cluster_word_frequency_vector(cluster.users)
        #         cluster_wf_vector = self.cluster_word_frequency_getter.get_cluster_word_frequency_by_ids(cluster.users)
        #         cluster_wf_vectors.append(cluster_wf_vector)
        #
        #         scores[i] = cluster_wf_vector.word_frequency_vector.cosine_sim_to(prev_wf_vector.word_frequency_vector)
        #
        #     # Sort word frequency vectors by similarity
        #     sorted_wf_vectors = list(sorted(scores, key=scores.get, reverse=True))
        #     closest_index = sorted_wf_vectors[0]
        #
        #     curr_cluster = clusters[closest_index]
        #     curr_wf_vector = cluster_wf_vectors[closest_index]
        # else:
        #     log.info("Picking Default Cluster")
        #     cluster = clusters[0]
        #     self.cluster_word_frequency_processor.process_cluster_word_frequency_vector(cluster.users)
        #
        #     curr_cluster = cluster
        #     curr_wf_vector = self.cluster_word_frequency_getter.get_cluster_word_frequency_by_ids(cluster.users)

        # Cluster Using Jaccard Set Similarity
        if prev_cluster is not None:
            log.info("Picking Cluster")
            similarities = {}
            for i in range(len(clusters)):
                cluster = clusters[i]
                similarities[i] = jaccard_similarity(prev_cluster.users, cluster.users)

            # Sort Jaccard similarities
            log.info("Similarities: ")
            log.info(similarities)
            sorted_similarities = list(sorted(similarities, key=similarities.get, reverse=True))

            closest_index = sorted_similarities[0]

            curr_cluster = clusters[closest_index]

        else:
            log.info("Picking Default Cluster")
            largest_index = 0
            for i in range(len(clusters)):
                cluster = clusters[i]
                if len(cluster.users) > len(clusters[largest_index].users):
                    largest_index = i

            curr_cluster = clusters[largest_index]

        log.info("The cluster chosen is: ")
        log.info(curr_cluster.users)

        log.info("Downloading Cluster Tweets")
        if str(user_id) not in downloaded_users:
            self.user_tweet_downloader.stream_tweets_by_user_list(curr_cluster.users)
            #self.user_tweet_downloader.download_user_tweets_by_user_list(curr_cluster.users)


        log.info("Downloading liked tweets")
        self.user_tweet_downloader.download_user_liked_tweets_by_user_list(curr_cluster.users)

        log.info("Ranking Cluster...")
        log.info("Computing Local Retweets Production")
        prod_ranking, prod = self.prod_ranker.rank(str(user_id), curr_cluster)
        log.info("Computing Local Retweets Consumption")
        con_ranking, con = self.con_ranker.rank(str(user_id), curr_cluster)
        log.info("Computing Local Likes Production")
        like_prod_ranking, prod_like = self.like_prod_ranker.rank(str(user_id), curr_cluster)
        log.info("Computing Local Likes Consumption")
        like_con_ranking, con_like = self.like_con_ranker.rank(str(user_id), curr_cluster)

        # prod_ranking = self.ranking_getter.get_ranking(str(user_id), params="retweets")
        # con_ranking = self.ranking_getter.get_ranking(str(user_id), params="consumption utility")

        # local_retweets = []
        # for retweet in self.user_tweet_getter.get_retweets_by_user_id_time_restricted("254201259"):
        #     if str(retweet.retweet_user_id) in curr_cluster.users and str(retweet.retweet_user_id) != "254201259":
        #         local_retweets.append(retweet)
        # log.info(len(local_retweets))
        # count = 0
        # for retweet in local_retweets:
        #     if str(retweet.retweet_user_id) in set([str(id) for id in friends]).intersection(curr_cluster.users):
        #         count += 1
        #     else:
        #         if str(retweet.retweet_user_id) not in curr_cluster.users:
        #             print("nope!")
        #         log.info(retweet.retweet_user_id)
        # log.info(count/len(local_retweets))
        top_10_prod = prod_ranking.get_top_10_user_ids()
        top_10_con = con_ranking.get_top_10_user_ids()
        top_10_prod_like = like_prod_ranking.get_top_10_user_ids()
        top_10_con_like = like_con_ranking.get_top_10_user_ids()
        log.info("Top 10 Local Retweet Production")
        log.info([self.user_getter.get_user_by_id(str(id)).screen_name for id in top_10_prod])
        log.info("Top 10 Local Retweet Consumption")
        log.info([self.user_getter.get_user_by_id(str(id)).screen_name for id in top_10_con])
        log.info("Top 10 Local Like Production")
        log.info([self.user_getter.get_user_by_id(str(id)).screen_name for id in top_10_prod_like])
        log.info("Top 10 Local Like Consumption")
        log.info([self.user_getter.get_user_by_id(str(id)).screen_name for id in top_10_con_like])

        top_20_prod = prod_ranking.get_top_20_user_ids()
        top_20_con = con_ranking.get_top_20_user_ids()
        top_20_prod_like = like_prod_ranking.get_top_20_user_ids()
        top_20_con_like = like_con_ranking.get_top_20_user_ids()
        log.info("Top 20 Local Retweet Production")
        log.info([self.user_getter.get_user_by_id(str(id)).screen_name for id in top_20_prod])
        log.info("Top 20 Local Retweet Consumption")
        log.info([self.user_getter.get_user_by_id(str(id)).screen_name for id in top_20_con])
        log.info("Top 20 Local Like Production")
        log.info([self.user_getter.get_user_by_id(str(id)).screen_name for id in top_20_prod_like])
        log.info("Top 20 Local Like Consumption")
        log.info([self.user_getter.get_user_by_id(str(id)).screen_name for id in top_20_con_like])

        top_50_prod = prod_ranking.get_top_50_user_ids()
        top_50_con = con_ranking.get_top_50_user_ids()
        top_50_prod_like = like_prod_ranking.get_top_50_user_ids()
        top_50_con_like = like_con_ranking.get_top_50_user_ids()
        log.info("Top 50 Prod")
        log.info([self.user_getter.get_user_by_id(str(id)).screen_name for id in top_50_prod])
        log.info("Top 50 Con")
        log.info([self.user_getter.get_user_by_id(str(id)).screen_name for id in top_50_con])
        log.info("Top 50 Local Like Production")
        log.info([self.user_getter.get_user_by_id(str(id)).screen_name for id in top_50_prod_like])
        log.info("Top 50 Local Like Consumption")
        log.info([self.user_getter.get_user_by_id(str(id)).screen_name for id in top_50_con_like])

        prod_top_50 = [prod[your_key] for your_key in top_50_prod]
        con_top_50 = [con[your_key] for your_key in top_50_con]
        con_like_top_50 = [con_like[your_key] for your_key in top_50_prod_like]
        prod_like_top_50 = [prod_like[your_key] for your_key in top_50_con_like]

        log.info("Generating Box plots and Histograms for Utility Functions...")
        generate_boxplot(prod_top_50, "Local_Retweet_Prod", count)
        generate_boxplot(con_top_50, "Local_Retweet_Con", count)
        generate_boxplot(con_like_top_50, "Local_Like_Prod", count)
        generate_boxplot(prod_like_top_50, "Local_Like_Con", count)
        generate_hist(prod_top_50, "Local_Retweet_Prod", count)
        generate_hist(con_top_50, "Local_Retweet_Con", count)
        generate_hist(con_like_top_50, "Local_Like_Prod", count)
        generate_hist(prod_like_top_50, "Local_Like_Con", count)

        intersection_50_likes = set(top_50_prod_like).intersection(top_50_con_like)
        intersection_50_likes_prod = sorted(intersection_50_likes, key=prod_like.get, reverse=True)
        intersection_50_likes_con = sorted(intersection_50_likes, key=con_like.get, reverse=True)

        log.info("Using Top 50, intersection of local like producton & consumption: ")
        log.info("Production Like:")
        log.info([self.user_getter.get_user_by_id(str(id)).screen_name for id in intersection_50_likes_prod])
        log.info("Consumption Like:")
        log.info([self.user_getter.get_user_by_id(str(id)).screen_name for id in intersection_50_likes_con])

        intersection_50_retweets = set(top_50_prod).intersection(top_50_con)
        intersection_50_retweets_prod = sorted(intersection_50_retweets, key=prod.get, reverse=True)
        intersection_50_retweets_con = sorted(intersection_50_retweets, key=con.get, reverse=True)

        log.info("Using Top 50, intersection of local retweet producton & consumption: ")
        log.info("Production Retweet:")
        log.info([self.user_getter.get_user_by_id(str(id)).screen_name for id in intersection_50_retweets_prod])
        log.info("Consumption Retweet:")
        log.info([self.user_getter.get_user_by_id(str(id)).screen_name for id in intersection_50_retweets_con])

        log.info("Plot top 50 Local Retweet Production, and their score in other utility function")
        prod_top_50_con = []
        prod_top_50_prod_like = []
        prod_top_50_con_like = []
        for top_user in top_50_prod:
            prod_top_50_con.append(con[top_user])
            prod_top_50_con_like.append(con_like[top_user])
            prod_top_50_prod_like.append(prod_like[top_user])
        generate_scatterplot("Top 50 Retweet Production", "Retweet Consumption",
                             prod_top_50, prod_top_50_con, count)
        generate_scatterplot("Top 50 Retweet Production", "Like Consumption",
                             prod_top_50, prod_top_50_con_like, count)
        generate_scatterplot("Top 50 Retweet Production", "Like Production",
                             prod_top_50, prod_top_50_prod_like, count)
        log.info("Plot top 50 Local Retweet Consumption, and their score in other utility function")
        con_top_50_prod = []
        con_top_50_prod_like = []
        con_top_50_con_like = []
        for top_user in top_50_con:
            con_top_50_prod.append(prod[top_user])
            con_top_50_con_like.append(con_like[top_user])
            con_top_50_prod_like.append(prod_like[top_user])
        generate_scatterplot("Top 50 Retweet Consumption", "Retweet Production",
                             con_top_50, con_top_50_prod, count)
        generate_scatterplot("Top 50 Retweet Consumption", "Like Consumption",
                             con_top_50, con_top_50_prod_like, count)
        generate_scatterplot("Top 50 Retweet Consumption", "Like Production",
                             con_top_50, con_top_50_con_like, count)
        log.info("Plot top 50 Local Like Consumption, and their score in other utility function")
        con_like_top_50_prod = []
        con_like_top_50_con = []
        con_like_top_50_prod_like = []
        for top_user in top_50_con_like:
            con_like_top_50_prod.append(prod[top_user])
            con_like_top_50_con.append(con[top_user])
            con_like_top_50_prod_like.append(prod_like[top_user])
        generate_scatterplot("Top 50 Like Consumption", "Retweet Production",
                             con_like_top_50, con_like_top_50_prod, count)
        generate_scatterplot("Top 50 Like Consumption", "Retweet Consumption",
                             con_like_top_50, con_like_top_50_con, count)
        generate_scatterplot("Top 50 Like Consumption", "Like Production",
                             con_like_top_50, con_like_top_50_prod_like, count)
        log.info("Plot top 50 Local Like Production, and their score in other utility function")
        prod_like_top_50_prod = []
        prod_like_top_50_con = []
        prod_like_top_50_con_like = []
        for top_user in top_50_prod_like:
            prod_like_top_50_prod.append(prod[top_user])
            prod_like_top_50_con.append(con[top_user])
            prod_like_top_50_con_like.append(con_like[top_user])
        generate_scatterplot("Top 50 Like Production", "Retweet Production",
                             prod_like_top_50, prod_like_top_50_prod, count)
        generate_scatterplot("Top 50 Like Production", "Retweet Consumption",
                             prod_like_top_50, prod_like_top_50_con, count)
        generate_scatterplot("Top 50 Like Production", "Like Consumption",
                             prod_like_top_50, prod_like_top_50_con_like, count)

        log.info("Analyzing all users in any intersection...")
        user_described = []
        for top_user in intersection_50_likes_prod:
            if top_user not in user_described:
                user_described.append(top_user)
                log.info(self.user_getter.get_user_by_id(str(top_user)).screen_name)
                if top_user in top_50_prod:
                    log.info(f'Local Retweet Production: {prod[top_user]} Rank: {top_50_prod.index(top_user)}')
                else:
                    log.info(f'Local Retweet Production: {prod[top_user]} Rank: Not in Top 50')
                if top_user in top_50_con:
                    log.info(f'Local Retweet Consumption: {con[top_user]} Rank: {top_50_con.index(top_user)}')
                else:
                    log.info(f'Local Retweet Consumption: {con[top_user]} Rank: Not in Top 50')
                log.info(f'Local Like Consumption: {con_like[top_user]} Rank: {top_50_con_like.index(top_user)}')
                log.info(f'Local Like Production: {prod_like[top_user]} Rank: {top_50_prod_like.index(top_user)}')
        for top_user in intersection_50_retweets_prod:
            if top_user not in user_described:
                user_described.append(top_user)
                log.info(self.user_getter.get_user_by_id(str(top_user)).screen_name)
                log.info(f'Local Retweet Production: {prod[top_user]} Rank: {top_50_prod.index(top_user)}')
                log.info(f'Local Retweet Consumption: {con[top_user]} Rank: {top_50_con.index(top_user)}')
                if top_user in top_50_con_like:
                    log.info(f'Local Like Consumption: {con_like[top_user]} Rank: {top_50_con_like.index(top_user)}')
                else:
                    log.info(f'Local Like Consumption: {con_like[top_user]} Rank: Not in Top 50')
                if top_user in top_50_prod_like:
                    log.info(f'Local Like Production: {prod_like[top_user]} Rank: {top_50_prod_like.index(top_user)}')
                else:
                    log.info(f'Local Like Production: {prod_like[top_user]} Rank: Not in Top 50')
        intersection_50_all = set(top_50_prod).intersection(top_50_con, top_50_con_like, top_50_prod_like)
        intersection_50_all_retweets_prod = sorted(intersection_50_all, key=prod.get, reverse=True)
        intersection_50_all_retweets_con = sorted(intersection_50_all, key=con.get, reverse=True)
        intersection_50_all_likes_prod = sorted(intersection_50_all, key=prod_like.get, reverse=True)
        intersection_50_all_likes_con = sorted(intersection_50_all, key=con_like.get, reverse=True)

        log.info("Using Top 50, intersection of all: ")
        log.info("Production Retweet:")
        log.info([self.user_getter.get_user_by_id(str(id)).screen_name for id in intersection_50_all_retweets_prod])
        log.info("Consumption Retweet:")
        log.info([self.user_getter.get_user_by_id(str(id)).screen_name for id in intersection_50_all_retweets_con])
        log.info("Production Like:")
        log.info([self.user_getter.get_user_by_id(str(id)).screen_name for id in intersection_50_all_likes_prod])
        log.info("Consumption Like:")
        log.info([self.user_getter.get_user_by_id(str(id)).screen_name for id in intersection_50_all_likes_con])

        penalty = 10
        log.info(f"Similarity Test with penalty {penalty}")


        # # TODO: PRODUCTION
        # # By Production
        # log.info("By Production")
        # curr_user_id = intersection_20_prod[0]
        #
        # if curr_user_id == str(user_id):
        #     if intersection_20_con[0] != curr_user_id:
        #         index = intersection_20_con.index(curr_user_id)
        #         for i in range(1, 20):
        #             temp_id = intersection_20_prod[i]
        #             if intersection_20_con.index(temp_id) < index:
        #                 curr_user_id = temp_id
        #                 break

        # TODO: CONSUMPTION
        # By Consumption
        # log.info("By Consumption")
        # curr_user_id = intersection_20_con[0]
        #
        # if curr_user_id == str(user_id):
        #     if intersection_20_prod[0] != curr_user_id:
        #         index = intersection_20_prod.index(curr_user_id)
        #         for i in range(1, 20):
        #             temp_id = intersection_20_con[i]
        #             if intersection_20_prod.index(temp_id) < index:
        #                 curr_user_id = temp_id
        #                 break

        # log.info("By Local Like Production")
        # curr_user_id = intersection_50_likes_prod[0]
        # log.info(f"Highest Rank User in Local Like Production is "
        #          f"{self.user_getter.get_user_by_id(str(curr_user_id)).screen_name}")
        # if curr_user_id == str(user_id):
        #     if intersection_50_likes_con[0] != curr_user_id:
        #         index = intersection_50_likes_con.index(curr_user_id)
        #         for i in range(1, 50):
        #             temp_id = intersection_50_likes_prod[i]
        #             if intersection_50_likes_con.index(temp_id) < index:
        #                 curr_user_id = temp_id
        #                 break
        log.info("By Local Consumption")

        curr_user_id = intersection_50_likes_con[0]
        if curr_user_id == str(user_id):
            if intersection_50_likes_prod[0] != curr_user_id:
                index = intersection_50_likes_prod.index(curr_user_id)
                for i in range(1, 20):
                    temp_id = intersection_50_likes_con[i]
                    if intersection_50_likes_prod.index(temp_id) < index:
                        curr_user_id = temp_id
                        break

        # TODO: LIKED
        # # By Like Utility Ranker
        # log.info("By like utility ranker")
        # curr_user_id = intersection_20_like[0]
        # # is the highest rank user the user we are looping from?
        # str123 = "high rank like user: "+ str(curr_user_id)+ "original user: " + str(user_id)
        # log.info(str123)
        # if curr_user_id == str(user_id):
        #     # is he also the highest rank user from production?
        #     log.info("Not highest rank from production")
        #     if intersection_20_prod[0] != curr_user_id:
        #         # if not find its rank in production
        #         index = intersection_20_prod.index(curr_user_id)
        #         for i in range(1, 20):
        #             # change highest rank to the highest rank user in like that has rank in production higher than index
        #             temp_id = intersection_20_like[i]
        #             if intersection_20_prod.index(temp_id) < index:
        #                 str123 = "Changed user to " + str(temp_id)+ " with rank "+ str(intersection_20_prod.index(temp_id))
        #                 log.info(str123)
        #                 curr_user_id = temp_id
        #                 break

        #generate_plot("Production", "Like", prod_ranking, prod, like_ranking, like, curr_user_id,count)
        #generate_plot("Consumption", "Production+Like", con_ranking, con, like_ranking, like, curr_user_id,count, self.user_getter)
        #generate_plot_2("Consumption", "Production", con_ranking, con, prod_ranking, prod, curr_user_id,count, self.user_getter)

        # curr_user_id = ranking.get_top_user_id()
        # top_ids = ranking.get_top_20_user_ids()
        # top_names = [self.user_getter.get_user_by_id(str(id)).screen_name for id in top_ids]
        # log.info("Top 20 users are: ")
        # log.info(top_names)
        curr_user_name = self.user_getter.get_user_by_id(str(curr_user_id)).screen_name
        log.info("Highest Ranking User is " + curr_user_name)
        # self.save_top_users(curr_cluster.users, top_names, self.user_getter.get_user_by_id(str(user_id)).screen_name, "production")

        return curr_user_id, curr_wf_vector, curr_cluster


    def save_top_users(self, cluster, users, seed_name, type):
        path = "./results/" + type + "/top_users/"

        if not os.path.exists(path):
            os.makedirs(path)
        filename = (path + seed_name + '.json')

        json_data = {
            'seed_name': seed_name,
            'top_20_users': users,
            'cluster': cluster
        }

        with open(filename, 'w+') as file:
            json.dump(json_data, file)

