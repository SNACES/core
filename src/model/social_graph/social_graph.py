import bson
import networkx as nx
from typing import Dict, Optional
from src.model.local_neighbourhood import LocalNeighbourhood


class SocialGraph():
    """
    A Wrapper class for a networkx graph representing a local neighbourhood
    """

    def __init__(self, graph: nx.Graph, seed_id: str, params=None):
        self.graph = graph
        self.seed_id = seed_id
        self.params = params

    def fromLocalNeighbourhood(local_neighbourhood: LocalNeighbourhood, params: Optional[Dict] = None):
        raise NotImplementedError("Subclasses should implement this")

    def fromDict(dict: Dict):
        adj_list = dict["adj_list"]
        graph = nx.parse_adjlist(adj_list)

        seed_id = dict["seed_id"]
        params = dict["params"]

        social_graph = SocialGraph(graph, seed_id, params)

    def toBSON(self):
        bson = {
            "seed_id": bson.int64.Int64(self.seed_id),
            "params": self.params,
            "adj_list": list(nx.generate_adjlist(self.graph))
        }

        return bson
