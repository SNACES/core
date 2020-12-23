import networkx as nx
from copy import deepcopy
from src.model.social_graph.social_graph import SocialGraph
from src.model.local_neighbourhood import LocalNeighbourhood


class IntersectionSocialGraph(SocialGraph):
    def fromLocalNeighbourhood(local_neighbourhood: LocalNeighbourhood, params=None):
        graph = nx.Graph()

        user_list = local_neighbourhood.get_user_id_list()
        for user in user_list:
            graph.add_node(user)

        for user in user_list:
            friends = local_neighbourhood.get_user_friends(user)
            for friend in friends:
                if user in local_neighbourhood.get_user_friends(friend):
                    graph.add_edge(user, friend)

        params = deepcopy(local_neighbourhood.params)
        if params is None:
            params = {}

        params["graph_type"] = "intersection"

        social_graph = SocialGraph(graph, local_neighbourhood.seed_id, params)
        return social_graph
