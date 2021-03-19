import networkx as nx
from copy import deepcopy
from src.model.social_graph.social_graph import SocialGraph
from src.model.local_neighbourhood import LocalNeighbourhood
from src.shared.logger_factory import LoggerFactory
import logging

log = LoggerFactory.logger(__name__, logging.INFO)


class UnionSocialGraph(SocialGraph):
    def fromLocalNeighbourhood(local_neighbourhood: LocalNeighbourhood, params=None):
        graph = nx.DiGraph()

        user_list = local_neighbourhood.get_user_id_list()
        user_list.remove(str(local_neighbourhood.seed_id))
        log.info("Length of list " + str(len(user_list)))
        for user in user_list:
            graph.add_node(user)

        for user in user_list:
            friends = local_neighbourhood.get_user_friends(user)
            for friend in friends:
                graph.add_edge(user, friend)

        params = deepcopy(local_neighbourhood.params)
        if params is None:
            params = {}

        params["graph_type"] = "union"

        social_graph = SocialGraph(graph, local_neighbourhood.seed_id, params)
        return social_graph
