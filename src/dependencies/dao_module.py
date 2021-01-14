from src.dao.cluster.cluster_dao_factory import ClusterDAOFactory
from src.dao.local_neighbourhood.local_neighbourhood_dao_factory import LocalNeighbourhoodDAOFactory
from src.dao.processed_tweet.processed_tweet_dao_factory import ProcessedTweetDAOFactory
from src.dao.ranking.ranking_dao_factory import RankingDAOFactory
from src.dao.raw_tweet.raw_tweet_dao_factory import RawTweetDAOFactory
from src.dao.social_graph.social_graph_dao_factory import SocialGraphDAOFactory
from src.dao.twitter.twitter_dao_factory import TwitterDAOFactory
from src.dao.user.user_dao_factory import UserDAOFactory
from src.dao.user_follower.user_follower_dao_factory import UserFollowerDAOFactory
from src.dao.user_friend.user_friend_dao_factory import UserFriendDAOFactory


class DAOModule():
    def __init__(self, config):
        input_datastore = config["input-datastore"]
        output_datastore = config["output-datastore"]
        inout_datastore = {}
        try:
            inout_datastore = config["inout-datastore"]
        except:
            pass

        # Set input datastore to be the union of input and inout
        # (with inout taking priority)
        self.input_datastore = input_datastore
        self.input_datastore.update(inout_datastore)

        # Set output datastore to be the union of output and inout
        # (with inout taking priority)
        self.output_datastore = output_datastore
        self.output_datastore.update(inout_datastore)

    def get_twitter_getter(self):
        return TwitterDAOFactory.create_getter(
            self.input_datastore["Download-Source"])

    def get_cluster_getter(self):
        return ClusterDAOFactory.create_getter(
            self.input_datastore["Clusters"])

    def get_cluster_setter(self):
        return ClusterDAOFactory.create_setter(
            self.output_datastore["Clusters"])

    def get_local_neighbourhood_getter(self):
        return LocalNeighbourhoodDAOFactory.create_getter(
            self.input_datastore["LocalNeighbourhoods"])

    def get_local_neighbourhood_setter(self):
        return LocalNeighbourhoodDAOFactory.create_setter(
            self.output_datastore["LocalNeighbourhoods"])

    def get_processed_tweet_getter(self):
        return ProcessedTweetDAOFactory.create_getter(
            self.input_datastore["ProcessedTweets"])

    def get_processed_tweet_setter(self):
        return ProcessedTweetDAOFactory.create_setter(
            self.output_datastore["ProcessedTweets"])

    def get_ranking_getter(self):
        return RankingDAOFactory.create_getter(
            self.input_datastore["Rankings"])

    def get_ranking_setter(self):
        return RankingDAOFactory.create_setter(
            self.output_datastore["Rankings"])

    def get_raw_tweet_getter(self):
        return RawTweetDAOFactory.create_getter(
            self.input_datastore["RawTweets"])

    def get_raw_tweet_setter(self):
        return RawTweetDAOFactory.create_setter(
            self.output_datastore["RawTweets"])

    def get_user_tweet_getter(self):
        return RawTweetDAOFactory.create_getter(
            self.input_datastore["UserTweets"])

    def get_user_tweet_setter(self):
        return RawTweetDAOFactory.create_setter(
            self.output_datastore["UserTweets"])

    def get_social_graph_getter(self):
        return SocialGraphDAOFactory.create_getter(
            self.input_datastore["SocialGraphs"])

    def get_social_graph_setter(self):
        return SocialGraphDAOFactory.create_setter(
            self.output_datastore["SocialGraphs"])

    def get_user_getter(self):
        return UserDAOFactory.create_getter(
            self.input_datastore["Users"])

    def get_user_setter(self):
        return UserDAOFactory.create_setter(
            self.output_datastore["Users"])

    def get_user_follower_getter(self):
        return UserFollowerDAOFactory.create_getter(
            self.input_datastore["Followers"])

    def get_user_follower_setter(self):
        return UserFollowerDAOFactory.create_setter(
            self.output_datastore["Followers"])

    def get_user_friend_getter(self):
        return UserFriendDAOFactory.create_getter(
            self.input_datastore["Friends"])

    def get_user_friend_setter(self):
        return UserFriendDAOFactory.create_setter(
            self.output_datastore["Friends"])
