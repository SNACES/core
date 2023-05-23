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
from src.dao.user_word_frequency.user_word_frequency_dao_factory import UserWordFrequencyDAOFactory
from src.dao.user_relative_word_frequency.user_relative_word_frequency_dao_factory import UserRelativeWordFrequencyDAOFactory
from src.dao.cluster_word_frequency.cluster_word_frequency_dao_factory import ClusterWordFrequencyDAOFactory
from src.dao.cluster_relative_word_frequency.cluster_relative_word_frequency_dao_factory import ClusterRelativeWordFrequencyDAOFactory
from src.dao.global_word_frequency.global_word_frequency_dao_factory import GlobalWordFrequencyDAOFactory
from src.dao.community.community_dao_factory import CommunityDAOFactory
from src.dao.user_friend.user_friend_from_tweets_dao_factory import UserFriendFromTweetsDAOFactory
from src.dao.local_neighbourhood.local_nbhd_from_tweets_dao_factory import LocalNbhdFromTweetsDAOFactory


class DAOModule():
    def __init__(self, config):
        input_datastore = config.get("input-datastore", {})
        output_datastore = config.get("output-datastore", {})
        inout_datastore = config.get("inout-datastore", {})

        # Set input datastore to be the union of input and inout
        # (with inout taking priority)
        self.input_datastore = input_datastore
        self.input_datastore.update(inout_datastore)

        # Set output datastore to be the union of output and inout
        # (with inout taking priority)
        self.output_datastore = output_datastore
        self.output_datastore.update(inout_datastore)

    def get_local_nbhd_from_tweets_getter(self):
        return LocalNbhdFromTweetsDAOFactory.create_getter(
            self.input_datastore["LocalNbhdFromTweets"])
    
    def get_local_nbhd_from_tweets_setter(self):
        return LocalNbhdFromTweetsDAOFactory.create_setter(
            self.output_datastore["LocalNbhdFromTweets"])

    def get_twitter_getter(self):
        return TwitterDAOFactory.create_getter(
            self.input_datastore["Download-Source"])

    def get_cluster_getter(self):
        return ClusterDAOFactory.create_getter(
            self.input_datastore["Cluster"])

    def get_cluster_setter(self):
        return ClusterDAOFactory.create_setter(
            self.output_datastore["Cluster"])

    def get_local_neighbourhood_getter(self):
        return LocalNeighbourhoodDAOFactory.create_getter(
            self.input_datastore["LocalNeighbourhood"])

    def get_local_neighbourhood_setter(self):
        return LocalNeighbourhoodDAOFactory.create_setter(
            self.output_datastore["LocalNeighbourhood"])

    def get_processed_tweet_getter(self):
        return ProcessedTweetDAOFactory.create_getter(
            self.input_datastore["ProcessedTweet"])

    def get_processed_tweet_setter(self):
        return ProcessedTweetDAOFactory.create_setter(
            self.output_datastore["ProcessedTweet"])

    def get_ranking_getter(self):
        return RankingDAOFactory.create_getter(
            self.input_datastore["Ranking"])

    def get_ranking_setter(self):
        return RankingDAOFactory.create_setter(
            self.output_datastore["Ranking"])

    def get_raw_tweet_getter(self):
        return RawTweetDAOFactory.create_getter(
            self.input_datastore["RawTweet"])

    def get_raw_tweet_setter(self):
        return RawTweetDAOFactory.create_setter(
            self.output_datastore["RawTweet"])

    def get_user_tweet_getter(self):
        return RawTweetDAOFactory.create_getter(
            self.input_datastore["UserTweet"])

    def get_user_tweet_setter(self):
        return RawTweetDAOFactory.create_setter(
            self.output_datastore["UserTweet"])

    def get_social_graph_getter(self):
        return SocialGraphDAOFactory.create_getter(
            self.input_datastore["SocialGraph"])

    def get_social_graph_setter(self):
        return SocialGraphDAOFactory.create_setter(
            self.output_datastore["SocialGraph"])

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
    
    def get_user_friend_from_tweets_getter(self):
        return UserFriendFromTweetsDAOFactory.create_getter(
            self.input_datastore["FriendsFromTweets"])
    
    def get_user_friend_from_tweets_setter(self):
        return UserFriendFromTweetsDAOFactory.create_setter(
            self.output_datastore["FriendsFromTweets"])

    def get_user_friend_getter(self):
        return UserFriendDAOFactory.create_getter(
            self.input_datastore["Friends"])

    def get_user_friend_setter(self):
        return UserFriendDAOFactory.create_setter(
            self.output_datastore["Friends"])

    def get_cleaned_user_friend_getter(self):
        return UserFriendDAOFactory.create_getter(
            self.input_datastore["CleanedFriends"])

    def get_cleaned_user_friend_setter(self):
        return UserFriendDAOFactory.create_setter(
            self.output_datastore["CleanedFriends"])

    def get_user_word_frequency_getter(self):
        return UserWordFrequencyDAOFactory.create_getter(
            self.input_datastore["UserWordFrequency"])

    def get_user_word_frequency_setter(self):
        return UserWordFrequencyDAOFactory.create_setter(
            self.output_datastore["UserWordFrequency"])

    def get_cluster_word_frequency_getter(self):
        return ClusterWordFrequencyDAOFactory.create_getter(
            self.input_datastore["ClusterWordFrequency"])

    def get_cluster_word_frequency_setter(self):
        return ClusterWordFrequencyDAOFactory.create_setter(
            self.output_datastore["ClusterWordFrequency"])

    def get_cluster_relative_word_frequency_getter(self):
        return ClusterRelativeWordFrequencyDAOFactory.create_getter(
            self.input_datastore["ClusterRelativeWordFrequency"])

    def get_cluster_relative_word_frequency_setter(self):
        return ClusterRelativeWordFrequencyDAOFactory.create_setter(
            self.output_datastore["ClusterRelativeWordFrequency"])

    def get_global_word_frequency_getter(self):
        return GlobalWordFrequencyDAOFactory.create_getter(
            self.input_datastore["GlobalWordFrequency"])

    def get_global_word_frequency_setter(self):
        return GlobalWordFrequencyDAOFactory.create_setter(
            self.output_datastore["GlobalWordFrequency"])

    def get_user_relative_word_frequency_getter(self):
        return UserRelativeWordFrequencyDAOFactory.create_getter(
            self.input_datastore["UserRelativeWordFrequency"])

    def get_user_relative_word_frequency_setter(self):
        return UserRelativeWordFrequencyDAOFactory.create_setter(
            self.output_datastore["UserRelativeWordFrequency"])
    
    def get_community_setter(self):
        return CommunityDAOFactory.create_setter(
            self.output_datastore["Community"])
