from src.dao.ranking.setter.ranking_setter import RankingSetter
from src.dao.ranking.setter.mongo_ranking_setter import MongoRankingSetter
from src.dao.ranking.getter.ranking_getter import RankingGetter
from src.dao.ranking.getter.mongo_ranking_getter import MongoRankingGetter
from src.shared.mongo import get_collection_from_config
from typing import Dict


class RankingDAOFactory():
    def create_getter(config: Dict) -> RankingGetter:
        ranking_getter = None
        if config["type"] == "Mongo":
            ranking_getter = MongoRankingGetter()
            collection = get_collection_from_config(config["config"])
            ranking_getter.set_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return ranking_getter

    def create_setter(config: Dict) -> RankingSetter:
        ranking_setter = None
        if config["type"] == "Mongo":
            ranking_setter = MongoRankingSetter()
            collection = get_collection_from_config(config["config"])
            ranking_setter.set_collection(collection)
        else:
            raise Exception("Datastore type not supported")

        return ranking_setter

