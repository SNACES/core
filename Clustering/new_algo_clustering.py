import sys
sys.path.append('../General')
sys.path.append('../General/Concrete-DAO')

from process import Process
from pymongo import MongoClient
from collections import Counter
from copy import deepcopy, copy
import datetime
from clustering import *
import numpy

class NewAlgoClustering(Process):
    # Database load and store wrappers
    # def process_cluster():
    #     pass

    # def process_prereq_data():
    #     pass



    # Main methods
    def detect_all_communities(self, user_to_items, item_to_users, user_count, item_count, is_only_popularity):
        id_to_cluster = {}
        count = 0
        # print(len(user_to_items))
        already_seen = []
        for user1 in user_to_items:
            for user2 in user_to_items:
                if user2 not in already_seen and user1 != user2:
                    item_intersection = list(set.intersection(
                        set(user_to_items[user1]), set(user_to_items[user2])))

                    if item_intersection != []:
                        cluster = self.detect_single_community(
                            user_to_items, item_to_users, item_intersection, user_count, item_count, is_only_popularity)
                        if cluster:
                            cluster_id = cluster['users']
                            if cluster_id not in id_to_cluster:
                                # print(cluster)
                                cluster['count'] = 1
                                id_to_cluster[cluster_id] = cluster
                                count += 1
                            else:
                                id_to_cluster[cluster_id]['count'] += 1

                            # print(count)

            already_seen.append(user1)

        return [id_to_cluster[cluster_id] for cluster_id in id_to_cluster]

    def detect_single_community(self, user_to_items, item_to_users, core_items, user_count, item_count, is_only_popularity):
        is_converged = False
        num_iterations = 0
        max_iterations = 10  # TODO: hyperparameter

        while not is_converged and num_iterations < max_iterations:
            tmp_core_items = deepcopy(core_items)
            # print(core_users)
            core_users = self.select(user_to_items, core_items, user_count, is_only_popularity)
            core_items = self.select(item_to_users, core_users, item_count, is_only_popularity)
            # print(core_items)
            # print(tmp_core_items)

            if tmp_core_items == core_items:
                is_converged = True

            num_iterations += 1

        core_users.sort()
        core_items.sort()
        return {'users': tuple(core_users), 'items': tuple(core_items)} if is_converged else None

    def select(self, user_to_items, core_items, count, is_only_popularity):
        # compute the popularity of each user wrt the core_items
        user_to_popularity = Counter()
        for user in user_to_items:
            intersect_count = len(set.intersection(
                set(core_items), set(user_to_items[user])))
            user_to_popularity[user] = intersect_count / len(core_items)

        if is_only_popularity:
            # get the top 5 most popular users
            popular_users = [user for user, popularity in user_to_popularity.most_common(count)]

            # consider tie cases
            possible_tie_value = user_to_popularity[popular_users[-1]]
            users_sorted_by_popularity = user_to_popularity.most_common()
            for i in range(count + 1, len(users_sorted_by_popularity)):
                user, popularity = users_sorted_by_popularity[i]
                if popularity == possible_tie_value:
                    popular_users.append(user)
                else:
                    return popular_users

            # popular_users.sort()
            return popular_users

        # compute the typicality of each user wrt the core_items
        user_to_typicality = Counter()
        for user in user_to_items:
            intersect_count = len(set.intersection(
                set(core_items), set(user_to_items[user])))
            user_to_typicality[user] = intersect_count / len(user_to_items[user])

        # compute the popularity and typicality rankings
        popularity_ranking = {pair[0]: rank
                            for rank, pair in enumerate(user_to_popularity.most_common())}

        typicality_ranking = {pair[0]: rank
                            for rank, pair in enumerate(user_to_typicality.most_common())}

        # compute the overall ranking for each user TODO: is there a bug with this?
        overall_ranking = Counter()
        for user in popularity_ranking:
            overall_ranking[user] = max(
                popularity_ranking[user], typicality_ranking[user])

        # TODO: consider tie cases 
        # get the top 5 overall ranking for users
        popular_users = [user[0] for user in overall_ranking.most_common()[-6:-1]]
        # popular_users = [user[0] for user in overall_ranking.most_common(5)]
        # for user in popular_users:
        # print(overall_ranking[user])
        popular_users.sort()
        return popular_users

    