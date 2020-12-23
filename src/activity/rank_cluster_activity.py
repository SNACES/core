from src.dao.cluster.cluster_dao_factory import ClusterDAOFactory
from src.dao.raw_tweet.raw_tweet_dao_factory import RawTweetDAOFactory
from src.process.ranking.retweets_ranker import RetweetsRanker
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

            self.ranker = RetweetsRanker(cluster_getter, raw_tweet_getter)

    def rank_cluster(self, seed_id, params):
        self.ranker.rank(seed_id, params)
