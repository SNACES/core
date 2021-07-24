from src.process.ranking.relative_production_ranker import RelativeProductionRanker
from src.dependencies.dao_module import DAOModule
from src.process.clustering.clusterer_factory import ClustererFactory
from src.process.core_detection.core_detector import CoreDetector
from src.process.community_detection.community_detection import CommunityDetector
from src.process.data_cleaning.friends_cleaner import FriendsCleaner
from src.process.data_cleaning.extended_friends_cleaner import ExtendedFriendsCleaner
from src.process.download.follower_downloader import TwitterFollowerDownloader
from src.process.download.friend_downloader import FriendDownloader
from src.process.download.local_neighbourhood_downloader import LocalNeighbourhoodDownloader
from src.process.download.local_neighbourhood_tweet_downloader import LocalNeighbourhoodTweetDownloader
from src.process.download.tweet_downloader import TwitterTweetDownloader
from src.process.download.user_downloader import TwitterUserDownloader
from src.process.download.user_tweet_downloader import UserTweetDownloader
from src.process.ranking.production_utility_ranker import ProductionUtilityRanker
from src.process.ranking.consumption_utility_ranker import ConsumptionUtilityRanker
from src.process.ranking.followers_ranker import FollowerRanker
from src.process.ranking.local_followers_ranker import LocalFollowersRanker
from src.process.community_ranking.community_production_ranker import CommunityProductionRanker
from src.process.community_ranking.community_consumption_ranker import CommunityConsumptionRanker
from src.process.community_ranking.linear_tweets_ranker import LinearCommunityRanker
from src.process.raw_tweet_processing.tweet_processor import TweetProcessor
from src.process.social_graph.social_graph_constructor import SocialGraphConstructor
from src.process.word_frequency.user_word_frequency_processor import UserWordFrequencyProcessor
from src.process.word_frequency.cluster_word_frequency_processor import ClusterWordFrequencyProcessor



class ProcessModule():
    """
    The process module is used to abstract the creation of processes, so they
    can be injected into classes which depend on them
    """

    def __init__(self, dao_module: DAOModule):
        self.dao_module = dao_module

    # Clustering
    def get_clusterer(self):
        social_graph_getter = self.dao_module.get_social_graph_getter()
        cluster_setter = self.dao_module.get_cluster_setter()
        user_friends_getter = self.dao_module.get_user_friend_getter() # TODO check whether we want this or cleaned_user_friend_getter()

        return ClustererFactory.create_clusterer("label_propagation",
            social_graph_getter, cluster_setter, user_friends_getter)

    # Core Detection
    def get_core_detector(self):
        user_getter = self.dao_module.get_user_getter()
        user_downloader = self.get_user_downloader()
        friend_downloader = self.get_friend_downloader()
        extended_friends_cleaner = self.get_extended_friends_cleaner()
        local_neighbourhood_downloader = self.get_local_neighbourhood_downloader()
        local_neighbourhood_tweet_downloader = self.get_local_neighbourhood_tweet_downloader()
        local_neighbourhood_getter = self.dao_module.get_local_neighbourhood_getter()
        tweet_processor = self.get_tweet_processor()
        social_graph_constructor = self.get_social_graph_constructor()
        clusterer = self.get_clusterer()
        cluster_getter = self.dao_module.get_cluster_getter()
        cluster_word_frequency_processor = self.get_cluster_word_frequency_processor()
        cluster_word_frequency_getter = self.dao_module.get_cluster_word_frequency_getter()
        prod_ranker = self.get_ranker() # Production
        con_ranker = self.get_ranker("Consumption")
        ranking_getter = self.dao_module.get_ranking_getter()
        user_tweet_downloader = self.get_user_tweet_downloader()
        user_tweet_getter = self.dao_module.get_user_tweet_getter()

        return CoreDetector(user_getter, user_downloader,
            friend_downloader, extended_friends_cleaner, local_neighbourhood_downloader,
            local_neighbourhood_tweet_downloader, local_neighbourhood_getter,
            tweet_processor, social_graph_constructor, clusterer, cluster_getter,
            cluster_word_frequency_processor, cluster_word_frequency_getter,
            prod_ranker, con_ranker, ranking_getter, user_tweet_downloader,
                            user_tweet_getter)

    def get_community_detector(self):
        user_getter = self.dao_module.get_user_getter()
        user_downloader = self.get_user_downloader()
        user_friends_downloader = self.get_friend_downloader()
        user_friends_getter = self.dao_module.get_user_friend_getter()
        user_tweets_downloader = self.get_user_tweet_downloader()
        community_setter = self.dao_module.get_community_setter()

        community_production_ranker = self.get_community_ranker(function_name="Production")
        community_consumption_ranker = self.get_community_ranker(function_name="Consumption")

        friends_cleaner = self.get_extended_friends_cleaner()
        cleaned_friends_getter = self.dao_module.get_cleaned_user_friend_getter()
        user_tweets_getter = self.dao_module.get_user_tweet_getter()

        return CommunityDetector(user_getter, user_downloader, user_friends_downloader,
            user_tweets_downloader, user_friends_getter, community_production_ranker,
            community_consumption_ranker, community_setter, friends_cleaner, cleaned_friends_getter, user_tweets_getter)

    # Data Cleaning
    def get_friends_cleaner(self):
        user_friend_getter = self.dao_module.get_user_friend_getter()
        cleaned_user_friend_setter = self.dao_module.get_cleaned_user_friend_setter()
        user_getter = self.dao_module.get_user_getter()

        friends_cleaner = FriendsCleaner(user_friend_getter,
            cleaned_user_friend_setter, user_getter)

        return friends_cleaner

    def get_extended_friends_cleaner(self):
        user_friend_getter = self.dao_module.get_user_friend_getter()
        cleaned_user_friend_setter = self.dao_module.get_cleaned_user_friend_setter()
        user_getter = self.dao_module.get_user_getter()
        consumption_ranker = self.get_ranker(type="Consumption")
        retweets_ranker = self.get_ranker()

        extended_friends_cleaner = ExtendedFriendsCleaner(user_friend_getter,
                cleaned_user_friend_setter, user_getter, consumption_ranker, retweets_ranker)

        return extended_friends_cleaner

    # Downloaduser_setter
    def get_follower_downloader(self):
        twitter_getter = self.dao_module.get_twitter_getter()
        user_follower_setter = self.dao_module.get_user_follower_setter()
        user_setter = self.dao_module.get_user_setter()

        follower_downloader = TwitterFollowerDownloader(twitter_getter, user_follower_setter,
            user_setter)

        return follower_downloader

    def get_friend_downloader(self):
        twitter_getter = self.dao_module.get_twitter_getter()
        user_friend_getter = self.dao_module.get_user_friend_getter()
        user_friend_setter = self.dao_module.get_user_friend_setter()
        user_setter = self.dao_module.get_user_setter()
        user_getter = self.dao_module.get_user_getter()

        friend_downloader = FriendDownloader(twitter_getter, user_friend_getter,
            user_friend_setter, user_setter, user_getter)

        return friend_downloader

    def get_local_neighbourhood_downloader(self):
        user_downloader = self.get_user_downloader()
        friend_downloader = self.get_friend_downloader()
        user_getter = self.dao_module.get_user_getter()
        user_friend_getter = self.dao_module.get_user_friend_getter()
        cleaned_user_friend_getter = self.dao_module.get_cleaned_user_friend_getter()
        local_neighbourhood_setter = self.dao_module.get_local_neighbourhood_setter()

        local_neighbourhood_downloader = LocalNeighbourhoodDownloader(user_downloader,
            friend_downloader, user_getter, user_friend_getter, cleaned_user_friend_getter, local_neighbourhood_setter)

        return local_neighbourhood_downloader

    def get_local_neighbourhood_tweet_downloader(self):
        user_tweet_downloader = self.get_user_tweet_downloader()
        local_neighbourhood_getter = self.dao_module.get_local_neighbourhood_getter()
        raw_tweet_getter = self.dao_module.get_user_tweet_getter()

        local_neighbourhood_tweet_downloader = LocalNeighbourhoodTweetDownloader(user_tweet_downloader,
            local_neighbourhood_getter, raw_tweet_getter)

        return local_neighbourhood_tweet_downloader

    def get_tweet_downloader(self):
        twitter_getter = self.dao_module.get_twitter_getter()
        raw_tweet_getter = self.dao_module.get_raw_tweet_setter()

        tweet_downloader = TwitterTweetDownloader(twitter_getter, raw_tweet_getter)

        return tweet_downloader

    def get_user_downloader(self):
        twitter_getter = self.dao_module.get_twitter_getter()
        user_setter = self.dao_module.get_user_setter()

        user_downloader = TwitterUserDownloader(twitter_getter, user_setter)

        return user_downloader

    def get_user_tweet_downloader(self):
        twitter_getter = self.dao_module.get_twitter_getter()
        user_tweet_setter = self.dao_module.get_user_tweet_setter()
        user_getter = self.dao_module.get_user_getter()

        print("User Getter is none? " + str(user_getter is None))

        user_tweet_downloader = UserTweetDownloader(twitter_getter, user_tweet_setter,
            user_getter)

        return user_tweet_downloader

    # Ranking TODO: Update to use ranker factory
    def get_ranker(self, type=None):
        cluster_getter = self.dao_module.get_cluster_getter()
        raw_tweet_getter = self.dao_module.get_user_tweet_getter()
        ranking_setter = self.dao_module.get_ranking_setter()
        user_getter = self.dao_module.get_user_getter()
        friends_getter = self.dao_module.get_user_friend_getter()

        if type == "Consumption":
            ranker = ConsumptionUtilityRanker(cluster_getter, raw_tweet_getter, ranking_setter)
        elif type == "Follower":
            ranker = FollowerRanker(cluster_getter, user_getter, ranking_setter)
        elif type == "LocalFollowers":
            ranker = LocalFollowersRanker(cluster_getter, user_getter, friends_getter, ranking_setter)
        elif type == "RelativeProduction":
            ranker = RelativeProductionRanker(cluster_getter, raw_tweet_getter, ranking_setter, user_getter)
        else:
            ranker = ProductionUtilityRanker(cluster_getter, raw_tweet_getter, ranking_setter)

        return ranker

    def get_community_ranker(self, function_name="Production"):
        user_tweets_getter = self.dao_module.get_user_tweet_getter()
        if function_name == "Consumption":
            ranker = CommunityConsumptionRanker(user_tweets_getter)
        elif function_name == "Production":
            ranker = CommunityProductionRanker(user_tweets_getter)
        elif function_name == 'linear':
            ranker = LinearCommunityRanker(user_tweets_getter)
        else:
            raise NotImplementedError("function name not identified")
        return ranker

    def get_followers_ranker(self):
        pass

    def get_retweets_ranker(self):
        pass

    # Processing
    def get_tweet_processor(self):
        raw_tweet_getter = self.dao_module.get_user_tweet_getter()
        processed_tweet_setter = self.dao_module.get_processed_tweet_setter()

        tweet_processor = TweetProcessor(raw_tweet_getter, processed_tweet_setter)

        return tweet_processor

    # Social Graph
    def get_social_graph_constructor(self):
        local_neighbourhood_getter = self.dao_module.get_local_neighbourhood_getter()
        social_graph_setter = self.dao_module.get_social_graph_setter()

        social_graph_constructor = SocialGraphConstructor(local_neighbourhood_getter, social_graph_setter)

        return social_graph_constructor


    # User Word Frequency
    def get_user_word_frequency_processor(self):
        processed_tweet_getter = self.dao_module.get_processed_tweet_getter()
        user_word_frequency_getter = self.dao_module.get_user_word_frequency_getter()
        user_word_frequency_setter = self.dao_module.get_user_word_frequency_setter()
        global_word_frequency_getter = self.dao_module.get_global_word_frequency_getter()
        user_relative_word_frequency_setter = self.dao_module.get_user_relative_word_frequency_setter()

        user_word_frequency_processor = UserWordFrequencyProcessor(processed_tweet_getter, user_word_frequency_getter,
            user_word_frequency_setter, global_word_frequency_getter, user_relative_word_frequency_setter)

        return user_word_frequency_processor

    def get_cluster_word_frequency_processor(self):
        user_word_frequency_getter = self.dao_module.get_user_word_frequency_getter()
        cluster_word_frequency_getter = self.dao_module.get_cluster_word_frequency_getter()
        cluster_word_frequency_setter = self.dao_module.get_cluster_word_frequency_setter()
        cluster_relative_word_frequency_setter = self.dao_module.get_cluster_relative_word_frequency_setter()
        global_word_frequency_getter = self.dao_module.get_global_word_frequency_getter()
        user_word_frequency_processor = self.get_user_word_frequency_processor()

        cluster_word_frequency_processor = ClusterWordFrequencyProcessor(user_word_frequency_getter, cluster_word_frequency_getter,
                                                                    cluster_word_frequency_setter, global_word_frequency_getter,
                                                                    cluster_relative_word_frequency_setter, user_word_frequency_processor)

        return cluster_word_frequency_processor
