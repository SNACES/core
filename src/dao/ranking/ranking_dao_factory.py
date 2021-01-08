from src.dao.ranking.setter.ranking_setter import RankingSetter
from src.dao.ranking.setter.mongo_ranking_setter import MongoRankingSetter
from src.dao.ranking.getter.ranking_getter import RankingGetter
from src.dao.ranking.getter.mongo_ranking_getter import MongoRankingGetter
from src.dao.mongo.mongo_dao_factory import MongoDAOFactory
from src.shared.mongo import get_collection_from_config
from typing import Dict


class RankingDAOFactory():
    def create_getter(config: Dict) -> RankingGetter:
        ranking_getter = None
        type = config["type"]
        if type == "Mongo":
            ranking_getter = MongoDAOFactory.create_getter(config["config"], MongoRankingGetter)
        else:
            raise Exception("Datastore type not supported")

        return ranking_getter

    def create_setter(config: Dict) -> RankingSetter:
        ranking_setter = None
        type = config["type"]
        if type == "Mongo":
            ranking_setter = MongoDAOFactory.create_setter(config["config"], MongoRankingSetter)
        else:
            raise Exception("Datastore type not supported")

        return ranking_setter
