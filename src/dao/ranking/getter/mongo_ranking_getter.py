from src.dao.ranking.getter.ranking_getter import RankingGetter
from src.dao.mongo.mongo_dao import MongoDAO


class MongoRankingGetter(RankingGetter, MongoDAO):
    pass
