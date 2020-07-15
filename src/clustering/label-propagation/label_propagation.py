import networkx as nx
from networkx.algorithms.community.modularity_max import greedy_modularity_communities
from networkx.algorithms.community.label_propagation import label_propagation_communities
import re
import sys
from datetime import datetime
from typing import List, Tuple, Union, Dict

import twitterDownloader

START_TIME = datetime(2019, 3, 1)
END_TIME = datetime(2020, 5, 1)


class LocalGraph():
    """A graph representing the local neighborhood of a particular user."""

    def __init__(self, output=sys.stdout) -> None:
        """Initializes a new LocalGraph."""
        self.graph = nx.Graph()
        self.base_user = None
        self.output = output

# implementation using tweepy - too slow, API-constrained
    def generate_from_user(self, user: str, ratio=None) -> None:
        """Populates the local graph with the local neighborhood of the given user."""
        self.base_user = user

        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/')
        col = client['productionFunction']['friendGraphs']
        query = col.find_one({"name": user})
        if query is not None:
            self.graph = nx.parse_adjlist(query['adj_list'])
        else:
            import os
            # note that we need to pass in full path
            ds_config_path = os.getcwd() + "/../General/ds-init-config.yaml"
            friends_downloader = twitterDownloader.TwitterFriendsDownloader(ds_config_path)
            friends_db = client['TwitterFriendsDownload']['getFriendsByScreenName']
            
            query = {'screen_name': user}
            user_friends_doc = friends_db.find_one(query)
            if user_friends_doc:
                user_friends_list = user_friends_doc['friends'] 
            else:
                user_friends_list = friends_downloader.get_friends_by_screen_name(user, -1, 'TweepyClient', 'getFriendsByScreenName')

            # local = [friend for friend in twitterDownloader.filter_out_bots(
            #          user_friends_list, START_TIME, END_TIME)] + [user]
            local = [user] + user_friends_list

            # nodes are friends of user
            for agent in local:
                self.graph.add_node(agent)

            # edges between user1 and user2 indicate that both users follow each other
            li = list(self.graph.nodes)
            for i in range(len(li)):
                for j in range(i, len(li)):
                    user1 = li[i]
                    user2 = li[j]

                    query = {'screen_name': user1}
                    user1_friends_doc = friends_db.find_one(query)
                    if user1_friends_doc:
                        user1_friends_list = user1_friends_doc['friends'] 
                    else:
                        user1_friends_list = friends_downloader.get_friends_by_screen_name(user1, -1, 'TweepyClient', 'getFriendsByScreenName')
                    
                    query = {'screen_name': user2}
                    user2_friends_doc = friends_db.find_one(query)
                    if user2_friends_doc:
                        user2_friends_list = user2_friends_doc['friends'] 
                    else:
                        user2_friends_list = friends_downloader.get_friends_by_screen_name(user2, -1, 'TweepyClient', 'getFriendsByScreenName')

                    if user1 in user2_friends_list and user2 in user1_friends_list:
                        self.graph.add_edge(li[j], li[i])

            adj_list = [item for item in nx.generate_adjlist(self.graph)]

            col.insert_one({"name": user, "adj_list": adj_list})
        
        # if ratio is not None:
        #     local = [friend for friend in db.filter_out_bots(db.get_friends(user), START_TIME, END_TIME)] + [user]
        #     local = db.cut_ratio_users(local, START_TIME, END_TIME, ratio)

        #     original_users = list(self.graph.nodes)
        #     for user in original_users:
        #         if user not in local:
        #             self.graph.remove_node(user)
    
    def get_clusters(self, method='modularity') -> Dict:
        """
        Returns a dictionary representation of the clusters of the local graph.
        """
        if method=='modularity':
            community_data = greedy_modularity_communities(self.graph)
        else:
            community_data = [item for item in label_propagation_communities(self.graph)]
        d = {}
        for i in range(len(community_data)):
            if self.base_user in community_data[i]:
                li = list(community_data[i])
                li.pop(li.index(self.base_user))
                li.insert(0, self.base_user)
                d[i] = li
            else:
                d[i] = [self.base_user] + list(community_data[i])

        return d

    def get_largest_cluster(self, method='modularity') -> List:
        """Returns the cluster of the local neighborhood that has the most users in it."""
        d = self.get_clusters(method)
        max_size = 0
        largest_cluster = []
        for key in d.keys():
            if len(d[key]) > max_size:
                largest_cluster = d[key]
                max_size = len(d[key])

        return largest_cluster

#     def match_community_to_keywords(self, community: str) -> List:
#         """
#         Returns the cluster of the local neighborhood that mostly closely corresponds to the keyword information
#         given by the community name.
#         """
#         d = self.get_clusters()
#         db = database_handler.DatabaseHandler()
#         keywords = db.get_keywords(community)
#         max_similarity_community = None
#         argmax_similarity_community = 0
#         for key in d.keys():
#             similarity_score = 0
#             num_tweets = 0
#             for user in d[key]:
#                 retweets, tweets = db.get_tweets(user, START_TIME, END_TIME)
#                 all_tweets = [retweet[0] for retweet in retweets] + tweets
#                 num_tweets += len(all_tweets)
#                 for tweet in all_tweets:
#                     if keywords_in_tweet(tweet, keywords):
#                         similarity_score += 1

#             similarity_score = 0 if num_tweets==0 else similarity_score/num_tweets

#             print('cluster being tested', max_similarity_community, 'score', similarity_score)

#             if argmax_similarity_community < similarity_score:
#                 max_similarity_community = d[key] if self.base_user in d[key] else d[key] + [self.base_user]
#                 argmax_similarity_community = similarity_score

#         #TODO remove from final product
#         print('max similarity community', max_similarity_community, 'score', similarity_score)
#         return max_similarity_community


# def keywords_in_tweet(tweet: str, keywords: List[str]) -> bool:
#     """
#     Helper function that returns true if a filtered version of a given tweet contains
#     a word in the set of keywords.
#     """
#     for keyword in keywords:
#         # A bit diff from sarah's regex but close enough
#         re_keyword = r'(?i)\b' + keyword + r's?\b'
#         if re.search(re_keyword, tweet) is not None:
#             return True
#     return False

if __name__=="__main__":
    lg = LocalGraph()
    lg.generate_from_user("animesh_garg")
    # clusters = lg.get_clusters(method='lprop')
    # print(clusters)
  