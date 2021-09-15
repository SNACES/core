import networkx as nx
from copy import deepcopy
from src.model.social_graph.social_graph import SocialGraph
from src.model.local_neighbourhood import LocalNeighbourhood
from src.shared.logger_factory import LoggerFactory
import logging

log = LoggerFactory.logger(__name__, logging.INFO)

class IntersectionSocialGraph(SocialGraph):
    def fromLocalNeighbourhood(local_neighbourhood: LocalNeighbourhood, params=None, remove_unconnected_nodes=True):
        graph = nx.DiGraph()

        user_list = local_neighbourhood.get_user_id_list()
        user_list.remove(str(local_neighbourhood.seed_id))
        log.info("Length of list " + str(len(user_list)))
        if remove_unconnected_nodes:
            user_list = SocialGraph.remove_unconnected_nodes(local_neighbourhood)
            log.info("Length of list after removing unconnected nodes " + str(len(user_list)))
            user_list.remove(str(local_neighbourhood.seed_id))

        for user in user_list:
            graph.add_node(user)

        for user in user_list:
            friends = local_neighbourhood.get_user_friends(user)
            for friend in friends:
                if friend != str(local_neighbourhood.seed_id):
                    if user in local_neighbourhood.get_user_friends(str(friend)):
                        graph.add_edge(user, friend)

        # Remove Unconnected Nodes
        remove = []
        for node in graph:
            neighbors = list(graph.neighbors(node))
            #predecessors = list(graph.predecessors(node))
            if len(neighbors) == 0:
                remove.append(node)
        for node in remove:
            graph.remove_node(node)

        params = deepcopy(local_neighbourhood.params)
        if params is None:
            params = {}

        params["graph_type"] = "intersection"

        social_graph = SocialGraph(graph, local_neighbourhood.seed_id, params)
        return social_graph
