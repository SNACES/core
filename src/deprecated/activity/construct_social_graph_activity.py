from src.dao.local_neighbourhood.local_neighbourhood_dao_factory import LocalNeighbourhoodDAOFactory
from src.dao.social_graph.social_graph_dao_factory import SocialGraphDAOFactory
from src.process.social_graph.social_graph_constructor import SocialGraphConstructor
from typing import Dict


class ConstructSocialGraphActivity():
    """

    """

    def __init__(self, config: Dict):
        self.social_graph_constructor = None

        self.configure(config)

    def configure(self, config: Dict):
        if config is not None:
            # Configure input datastore
            input_datastore = config["input-datastore"]
            local_neighbourhood = input_datastore["LocalNeighbourhood"]

            local_neighbourhood_getter = LocalNeighbourhoodDAOFactory.create_getter(local_neighbourhood)

            # Configure output datastore
            output_datastore = config["output-datastore"]
            social_graph = output_datastore["SocialGraph"]

            social_graph_setter = SocialGraphDAOFactory.create_setter(social_graph)

            self.social_graph_constructor = SocialGraphConstructor(local_neighbourhood_getter, social_graph_setter)

    def construct_social_graph(self, seed_id: str, params=None):
        self.social_graph_constructor.construct_social_graph_from_local_neighbourhood(seed_id, params)
