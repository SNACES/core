from src.dao.cluster.cluster_dao_factory import ClusterDAOFactory
from src.dao.raw_tweet.raw_tweet_dao_factory import RawTweetDAOFactory
from src.dao.ranking.ranking_dao_factory import RankingDAOFactory
from src.process.ranking.production_utility_ranker import ProductionUtilityRanker
from typing import Dict


class RankClusterActivity():
    """
    """

    def __init__(self, config: Dict):
        self.clusterer = None

        self.configure(config)

    def configure(self, config: Dict):
        if config is not None:
            # Configure input datastore
            input_datastore = config["input-datastore"]

            cluster = input_datastore["Cluster"]
            raw_tweet = input_datastore["RawTweet"]

            cluster_getter = ClusterDAOFactory.create_getter(cluster)
            raw_tweet_getter = RawTweetDAOFactory.create_getter(raw_tweet)

            # Configure output datastore
            output_datastore = config["output-datastore"]

            ranking = output_datastore["Ranking"]

            ranking_setter = RankingDAOFactory.create_setter(ranking)

            self.ranker = ProductionUtilityRanker(cluster_getter, raw_tweet_getter, ranking_setter)

    def rank_cluster(self, seed_id, params):
        self.ranker.rank(seed_id, params)
