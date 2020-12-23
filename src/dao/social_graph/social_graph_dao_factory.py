from src.dao.social_graph.setter.social_graph_setter import SocialGraphSetter
from src.dao.social_graph.setter.mongo_social_graph_setter import MongoSocialGraphSetter
from src.dao.social_graph.getter.social_graph_getter import SocialGraphGetter
from src.dao.social_graph.getter.mongo_social_graph_getter import MongoSocialGraphGetter
from src.dao.mongo.mongo_dao_factory import MongoDAOFactory
from typing import Dict


class SocialGraphDAOFactory():
    def create_getter(config: Dict) -> SocialGraphGetter:
        social_graph_getter = None
        type = config["type"]
        if type == "Mongo":
            social_graph_getter = MongoDAOFactory.create_getter(config["config"], MongoSocialGraphGetter)
        else:
            raise Excetpion("Datastore type not supported")

        return social_graph_getter

    def create_setter(config: Dict) -> SocialGraphSetter:
        social_graph_setter = None
        type = config["type"]
        if type == "Mongo":
            social_graph_setter = MongoDAOFactory.create_setter(config["config"], MongoSocialGraphSetter)
        else:
            raise Excetpion("Datastore type not supported")

        return social_graph_setter
