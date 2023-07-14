import networkx as nx
from copy import deepcopy
from src.model.social_graph.social_graph import SocialGraph
from src.model.local_neighbourhood import LocalNeighbourhood
from src.shared.logger_factory import LoggerFactory
import logging

log = LoggerFactory.logger(__name__, logging.INFO)


class UnionSocialGraph(SocialGraph):
    def fromLocalNeighbourhood(local_neighbourhood: LocalNeighbourhood, params=None,
                               weights_map=None,
                               remove_unconnected_nodes=True):
        graph = nx.DiGraph()

        user_list = local_neighbourhood.get_user_id_list()
        if str(local_neighbourhood.seed_id) in user_list:
            user_list.remove(str(local_neighbourhood.seed_id))
        log.info("Length of list " + str(len(user_list)))

        if remove_unconnected_nodes:
            user_list = SocialGraph.remove_unconnected_nodes(local_neighbourhood)
            log.info("Length of list after removing unconnected nodes " + str(len(user_list)))
            if str(local_neighbourhood.seed_id) in user_list:
                user_list.remove(str(local_neighbourhood.seed_id))
            # user_list.remove(str(local_neighbourhood.seed_id))

        for user in user_list:
            graph.add_node(user)

        for user in user_list:
            # In this case, user activities are (always) friends 
            friends = local_neighbourhood.get_user_activities(user)
            for friend in friends:
                if weights_map is not None:
                    graph.add_edge(user, str(friend), weight=weights_map[user][friend])
                else:
                    graph.add_edge(user, str(friend))
                    
        # Seed user may be re-introduced
        log.info(graph.order())

        params = deepcopy(local_neighbourhood.params)
        if params is None:
            params = {}

        params["graph_type"] = "union"

        social_graph = SocialGraph(graph, local_neighbourhood.seed_id, params)
        return social_graph
