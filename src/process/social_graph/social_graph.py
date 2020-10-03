import networkx as nx

class SocialGraph():
    """
    Creates a graph of twitter friends representing a community
    """

    def gen_user_friends_graph(self, user: str, user_friends_getter, social_graph_setter):
        """
        Generates a user friends graph for a given user

        @param user the user to generate the graph for
        @param user_friends_getter the dao to retrieve the given users friends from
        @param social_graph_setter the dao to store the computed social graph
        """
        user_friends_graph = self.get_user_friends_graph(user, user_friends_getter)
        social_graph_setter.store_user_friends_graph(user, user_friends_graph)

        return user_friends_graph

    def get_user_friends_graph(self, user: str, user_friends_getter) -> nx.Graph:
        """
        Constructs the social graph of a given user, assuming that the users local 
        neighbourhood has already been stored, and is accessible from user_friends_getter
        
        @param user the user to generate the graph for
        @param user_friends_getter the dao to retrieve the user's friends from

        @return the social graph of the user's local neighbourhood
        """
        graph = nx.Graph()
        user_friends_list = user_friends_getter.get_friends_by_name(user)
        local = [user] + user_friends_list

        # Nodes are friends of user
        for agent in local:
            graph.add_node(agent)

        # Edges between user1 and user2 indicate that both users follow each other
        li = list(graph.nodes)
        for i in range(len(li)):
            for j in range(i, len(li)):
                user1 = li[i]
                user2 = li[j]

                user1_friends_list = user_friends_getter.get_friends_by_name(user1)
                user2_friends_list = user_friends_getter.get_friends_by_name(user2)
            
                if user1 in user2_friends_list and user2 in user1_friends_list:
                    graph.add_edge(li[j], li[i])

        return graph
        
        # if ratio is not None:
        #     local = [friend for friend in db.filter_out_bots(db.get_friends(user), START_TIME, END_TIME)] + [user]
        #     local = db.cut_ratio_users(local, START_TIME, END_TIME, ratio)

        #     original_users = list(self.graph.nodes)
        #     for user in original_users:
        #         if user not in local:
        #             self.graph.remove_node(user)
