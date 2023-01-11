#!/usr/bin/env python
import click
import re

from src.shared.utils import get_project_root
from src.tools.user_list_processor import UserListProcessor
# Setup
from src.dependencies.injector import Injector

# Download
import src.tools.download_daemon as download_daemon
from src.shared.utils import get_date
from src.process.download.twitter_downloader import TwitterTweetDownloader, \
    TwitterFriendsDownloader, TwitterFollowersDownloader
from src.process.download.download_config_parser import DownloadConfigParser

# Raw Tweet Processing
from src.process.raw_tweet_processing.raw_tweet_processor import \
    RawTweetProcessor
from src.process.raw_tweet_processing.rt_processing_config_parser import \
    RawTweetProcessingConfigParser

# Word Frequency
from src.process.word_frequency.word_frequency import WordFrequency
from src.process.word_frequency.wf_config_parser import \
    WordFrequencyConfigParser

# Social Graph
from src.process.social_graph.social_graph import SocialGraph
from src.process.social_graph.social_graph_config_parser import \
    SocialGraphConfigParser

# Affinity Propagation
from src.process.clustering.affinity_propagation.affinity_propagation import \
    AffinityPropagation
from src.process.clustering.affinity_propagation.ap_config_parser import \
    AffinityPropagationConfigParser

# Label Propagation
from src.process.clustering.label_propagation.label_propagation import \
    LabelPropagation
from src.process.clustering.label_propagation.lp_config_parser import \
    LabelPropagationConfigParser

# MUISI
from src.process.clustering.MUISI.standard.muisi import MUISI, MUISIConfig
from src.process.clustering.MUISI.muisi_config_parser import MUISIConfigParser

# MUISI Retweets
from src.process.clustering.MUISI.retweets.muisi_retweet import MUISIRetweet, \
    MUISIRetweetConfig

# Community Expansion
from src.process.community_expansion.community_expansion import \
    CommunityExpansionAlgorithm
from src.process.ranking.influence_one_ranker import InfluenceOneRanker
from src.process.ranking.influence_two_ranker import InfluenceTwoRanker
from src.process.ranking.consumption_utility_ranker import \
    ConsumptionUtilityRanker
from src.process.ranking.production_utility_ranker import \
    ProductionUtilityRanker
from src.process.data_analysis.dataset_creator import DatasetCreator
from src.process.community_expansion.core_refiner import CoreRefiner
from src.process.data_analysis.graph_creator import GraphCreator


# CLI Helpers
def get_user():
    ulp = None
    use_user_list = click.confirm("Do you wish to provide a user list?")
    if use_user_list:
        default_ul_path = get_project_root() / 'src' / 'tools' / 'user_list'
        ul_path = click.prompt("User List Path", default_ul_path)
        ulp = UserListProcessor()
        user_or_user_list = ulp.user_list_parser(ul_path)
    else:
        user_or_user_list = click.prompt("User")

    return use_user_list, user_or_user_list, ulp


# Event handlers
def run_download():
    click.echo(
        "Provide the full path the the download config(leave blank to set to default)")
    default_path = get_project_root() / 'src' / 'process' / 'download' / 'download_config.yaml'
    download_config_path = click.prompt("Path", default_path)
    download_config_parser = DownloadConfigParser(download_config_path)
    tweepy_getter, user_friends_getter = download_config_parser.create_getter_DAOs()
    tweet_mongo_setter, user_friends_setter, user_followers_setter = download_config_parser.create_setter_DAOs()

    click.echo("Download Types:")
    click.echo("1. Twitter Tweet Download")
    click.echo("2. Twitter Friends Download")
    click.echo("3. Twitter Followers Download")
    download_type = click.prompt("Choose a download type", type=int)

    if download_type == 1:
        tweet_downloader = TwitterTweetDownloader()
        click.echo("Tweet types:")
        click.echo("1. User Tweets")
        click.echo("2. Random Tweets")
        tweet_type = click.prompt("Choose what to download", type=int)
        if tweet_type == 1:
            # TODO: follow by this example
            click.echo("Downloading User Tweets")
            use_user_list, user_or_user_list, ulp = get_user()
            num_tweets = click.prompt(
                "Number of Tweets(leave blank to get all)", type=int)
            if click.confirm("Do you want to specify a start and end date?"):
                start_date = get_date(click.prompt("Start Date(YYYY-MM-DD)"))
                end_date = get_date(click.prompt("End Date(YYYY-MM-DD)"))
                if use_user_list:
                    ulp.run_function_by_user_list(
                        tweet_downloader.gen_user_tweets, user_or_user_list,
                        tweepy_getter, tweet_mongo_setter, num_tweets,
                        start_date, end_date)
                else:
                    tweet_downloader.gen_user_tweets(user_or_user_list,
                                                     tweepy_getter,
                                                     tweet_mongo_setter,
                                                     num_tweets, start_date,
                                                     end_date)
            else:
                if use_user_list:
                    ulp.run_function_by_user_list(
                        tweet_downloader.gen_user_tweets, user_or_user_list,
                        tweepy_getter, tweet_mongo_setter, num_tweets)
                else:
                    tweet_downloader.gen_user_tweets(user_or_user_list,
                                                     tweepy_getter,
                                                     tweet_mongo_setter,
                                                     num_tweets)
        elif tweet_type == 2:
            click.echo("Downloading Random Tweets")
            click.echo(
                "Due to Tweepy constraints, if you want to download multiple tweets, you should launch a daemon")
            if click.confirm(
                    "Do you wish to launch a daemon to download random tweets?"):
                click.echo("Launching daemon")
                download_daemon.download_random_tweet()
            else:
                tweet_downloader.gen_random_tweet(tweepy_getter,
                                                  tweet_mongo_setter)
    elif download_type == 2:
        click.echo("Friend Download Types")
        click.echo("1. User Friends")
        click.echo("2. User Local Neighborhood")
        friend_type = click.prompt("Choose which to download", type=int)

        friends_downloader = TwitterFriendsDownloader()
        if friend_type == 1:
            click.echo("Downloading user friends")
            use_user_list, user_or_user_list, ulp = get_user()
            num_friends = click.prompt(
                "Number of Friends(leave blank to get all)", type=int)
            if use_user_list:
                ulp.run_function_by_user_list(
                    friends_downloader.gen_friends_by_screen_name,
                    user_or_user_list, tweepy_getter, user_friends_setter,
                    num_friends)
            else:
                friends_downloader.gen_friends_by_screen_name(user_or_user_list,
                                                              tweepy_getter,
                                                              user_friends_setter,
                                                              num_friends)
        elif friend_type == 2:
            click.echo("Downloading user local neightborhood")
            use_user_list, user_or_user_list, ulp = get_user()
            if use_user_list:
                ulp.run_function_by_user_list(
                    friends_downloader.gen_user_local_neighborhood,
                    user_or_user_list, tweepy_getter, user_friends_getter,
                    user_friends_setter)
            else:
                friends_downloader.gen_user_local_neighborhood(
                    user_or_user_list, tweepy_getter, user_friends_getter,
                    user_friends_setter)
        else:
            raise Exception("Invalid input")
    elif download_type == 3:
        click.echo("Downloading followers")
        use_user_list, user_or_user_list, ulp = get_user()
        num_followers = click.prompt(
            "Number of Followers(leave blank to get all)", type=int)
        followers_downloader = TwitterFollowersDownloader()
        if use_user_list:
            ulp.run_function_by_user_list(
                followers_downloader.gen_followers_by_screen_name,
                user_or_user_list, tweepy_getter, user_followers_setter,
                num_followers)
        else:
            followers_downloader.gen_followers_by_screen_name(user_or_user_list,
                                                              tweepy_getter,
                                                              user_followers_setter,
                                                              num_followers)
    else:
        raise Exception("Invalid input")


def run_rt_processing():
    click.echo(
        "Provide the full path the the raw tweet processing config(leave blank to set to default)")
    default_path = get_project_root() / 'src' / 'process' / 'raw_tweet_processing' / 'rt_processing_config.yaml'
    rt_processing_config_path = click.prompt("Path", default_path)
    rt_processing_config_parser = RawTweetProcessingConfigParser(
        rt_processing_config_path)
    tweet_getter = rt_processing_config_parser.create_getter_DAOs()
    tweet_setter, processed_tweet_setter = rt_processing_config_parser.create_setter_DAOs()
    tweet_processor = RawTweetProcessor()

    click.echo("Process Types")
    click.echo("1. Global(random) Tweets")
    click.echo("2. User Tweets")
    process_type = click.prompt("Choose what to process", type=int)

    if process_type == 1:
        click.echo("Processing global tweets")
        tweet_processor.gen_processed_global_tweets(tweet_getter, tweet_setter,
                                                    processed_tweet_setter)
    elif process_type == 2:
        click.echo("Processing user tweets")
        tweet_processor.gen_processed_user_tweets(tweet_getter, tweet_setter,
                                                  processed_tweet_setter)
    else:
        raise Exception("Invalid input")


def run_wf():
    default_path = get_project_root() / 'src' / 'process' / 'word_frequency' / 'wf_config.yaml'
    wf_config_path = click.prompt("Path", default_path)
    wf_config_parser = WordFrequencyConfigParser(wf_config_path)
    processed_tweet_getter, wf_getter = wf_config_parser.create_getter_DAOs()
    processed_tweet_setter, wf_setter = wf_config_parser.create_setter_DAOs()
    word_freq = WordFrequency()

    click.echo("Word Vector Types")
    click.echo("1. Global Word Count Vector")
    click.echo("2. Global Word Frequency Vector")
    click.echo("3. User Word Count Vector")
    click.echo("4. User Word Frequency Vector")
    click.echo("5. Relative User Word Frequency Vector")
    wf_type = click.prompt("Choose what to compute", type=int)

    if wf_type == 1:
        click.echo("Computing global word count vector")
        word_freq.gen_global_word_count_vector(processed_tweet_getter,
                                               processed_tweet_setter,
                                               wf_setter)
    elif wf_type == 2:
        click.echo("Computing global word frequency vector")
        word_freq.gen_global_word_frequency_vector(wf_getter, wf_setter)
    elif wf_type == 3:
        click.echo("Computing user word count vector")
        word_freq.gen_user_word_count_vector(processed_tweet_getter,
                                             processed_tweet_setter, wf_setter)
    elif wf_type == 4:
        click.echo("Computing user word frequency vector")
        word_freq.gen_user_word_frequency_vector(wf_getter, wf_setter)
    elif wf_type == 5:
        click.echo("Computing relative user word frequency vector")
        word_freq.gen_relative_user_word_frequency_vector(wf_getter, wf_setter)


def run_social_graph():
    default_path = get_project_root() / 'src' / 'process' / 'social_graph' / 'social_graph_config.yaml'
    social_graph_path = click.prompt("Path", default_path)
    social_graph_config_parser = SocialGraphConfigParser(social_graph_path)
    user_friends_getter = social_graph_config_parser.create_getter_DAOs()
    social_graph_setter = social_graph_config_parser.create_setter_DAOs()
    social_graph = SocialGraph()

    click.echo("Social Graph options")
    click.echo("1. User Friends Graph")
    social_graph_option = click.prompt("Choose what to compute", type=int)

    if social_graph_option == 1:
        click.echo("Computing user friends graph")
        click.echo(
            "Reminder: make sure to have downloaded the local neighborhood for your user of interest")
        use_user_list, user_or_user_list, ulp = get_user()
        if use_user_list:
            ulp.run_function_by_user_list(social_graph.gen_user_friends_graph,
                                          user_or_user_list,
                                          user_friends_getter,
                                          social_graph_setter)
        else:
            social_graph.gen_user_friends_graph(user_or_user_list,
                                                user_friends_getter,
                                                social_graph_setter)
    else:
        raise Exception("Invalid input")


def run_clustering():
    click.echo("Clustering Algorithms")
    click.echo("1. Affinity Propagation")
    click.echo("2. Label Propagation")
    click.echo("3. MUISI")
    clustering_type = click.prompt("Choose a clustering algorithm", type=int)

    if clustering_type == 1:
        click.echo("Computing Affinity Propagation cluster")
        ap = AffinityPropagation()
        default_path = get_project_root() / 'src' / 'process' / 'clustering' / 'affinity_propagation' / 'ap_config.yaml'
        ap_config_path = click.prompt("Path", default_path)
        ap_config_parser = AffinityPropagationConfigParser(ap_config_path)
        wf_getter = ap_config_parser.create_getter_DAOs()
        ap_setter = ap_config_parser.create_setter_DAOs()
        ap.gen_clusters(wf_getter, ap_setter)
    elif clustering_type == 2:
        click.echo("Computing Label Propagation cluster")
        default_path = get_project_root() / 'src' / 'process' / 'clustering' / 'label_propagation' / 'lp_config.yaml'
        lp_config_path = click.prompt("Path", default_path)
        lp_config_parser = LabelPropagationConfigParser(lp_config_path)
        social_graph_getter = lp_config_parser.create_getter_DAOs()
        lp_cluster_setter = lp_config_parser.create_setter_DAOs()
        user = click.prompt("User")
        lab_prop = LabelPropagation()
        lab_prop.gen_clusters(user, social_graph_getter, lp_cluster_setter)
    elif clustering_type == 3:
        click.echo("MUISI Variants")
        click.echo("1. Tweets")
        click.echo("2. Retweets")
        muisi_variant = click.prompt("Choose a variant", type=int)

        if muisi_variant == 1:
            click.echo("Computing MUISI cluster")
            default_path = get_project_root() / 'src' / 'process' / 'clustering' / 'muisi' / 'standard' / 'muisi_config.yaml'
            muisi_config_path = click.prompt("Path", default_path)
            muisi_config_parser = MUISIConfigParser(muisi_config_path, False)
            wf_getter = muisi_config_parser.create_getter_DAOs()
            muisi_cluster_setter = muisi_config_parser.create_setter_DAOs()
            muisi = MUISI()

            # Get user args
            intersection_min = click.prompt("Intersection Min", type=float)
            popularity = click.prompt("Popularity", type=float)
            threshold = click.prompt("Threshold", type=float)
            user_count = click.prompt("User Count", type=int)
            item_count = click.prompt("Item Count", type=int)
            count = click.prompt("Count", type=int)
            is_only_popularity = click.confirm(
                "Do you wish to only compute based on popularity?")
            muisi_config = MUISIConfig(intersection_min, popularity, threshold,
                                       user_count, item_count, count,
                                       is_only_popularity)

            muisi.gen_clusters(muisi_config, wf_getter, muisi_cluster_setter)
        elif muisi_variant == 2:
            click.echo("Computing MUISI retweets cluster")
            default_path = get_project_root() / 'src' / 'process' / 'clustering' / 'muisi' / 'retweets' / 'muisi_retweets_config.yaml'
            muisi_config_path = click.prompt("Path", default_path)
            muisi_config_parser = MUISIConfigParser(muisi_config_path, True)
            tweet_getter = muisi_config_parser.create_getter_DAOs()
            muisi_cluster_setter = muisi_config_parser.create_setter_DAOs()
            muisi = MUISIRetweet()

            # Get user args
            intersection_min = click.prompt("Intersection Min", type=float)
            popularity = click.prompt("Popularity", type=float)
            user_count = click.prompt("User Count", type=int)
            muisi_config = MUISIRetweetConfig(intersection_min, popularity,
                                              user_count)

            muisi.gen_clusters(muisi_config, tweet_getter, muisi_cluster_setter)
        else:
            raise Exception("Invalid input")
    else:
        raise Exception("Invalid input")


def run_community_expansion(process_module, dao_module):
    click.echo("Community Expansion")
    click.echo("Assume initial users are CORE users. "
               "The cleaner initial users are, the better expansion result.")

    threshold = 0.2
    top_size = 5
    candidates_size = 40
    large_account_threshold = 1.5
    num_of_candidate = 200
    core_size = 20
    ranker_list = []
    initial_user_list = ['228792418', '29843511', '5620142', '2895499182',
                         '1290762290224984064', '731538535795163136', '48642190',
                         '911297187664949248', '3333052551', '476582730']
    file_path = str(get_project_root()) + "/data/community_expansion/"

    run_default = click.prompt("Run default test?(y/n)", type=str)
    if run_default == "y":
        ranker_list.append(InfluenceOneRanker(
            dao_module.get_user_tweet_getter(),
            dao_module.get_user_friend_getter(),
            dao_module.get_ranking_setter()))
        ranker_list.append(InfluenceTwoRanker(
            dao_module.get_user_tweet_getter(),
            dao_module.get_user_friend_getter(),
            dao_module.get_ranking_setter()))
        ranker_list.append(ProductionUtilityRanker(
            dao_module.get_user_tweet_getter(),
            dao_module.get_user_friend_getter(),
            dao_module.get_ranking_setter()))
        ranker_list.append(ConsumptionUtilityRanker(
            dao_module.get_user_tweet_getter(),
            dao_module.get_user_friend_getter(),
            dao_module.get_ranking_setter()))
    else:
        click.echo("Initial User Types:")
        click.echo("1. Provide initial userid list")
        click.echo("2. Provide initial username list")
        initial_user_type = click.prompt("Choose an initial user type", type=int)
        if initial_user_type == 1:
            click.echo("Example: ")
            click.echo("The following are top 10 users calculated "
                       "by intersection ranking of influence one, influence two, "
                       "production, consumption by Core Detector.")
            click.echo("You can use them for practicing Community Expansion.")
            click.echo("ML community:")
            click.echo(['228792418', '29843511', '5620142', '2895499182',
                        '1290762290224984064', '731538535795163136', '48642190',
                        '911297187664949248', '3333052551', '476582730'])
            click.echo("Chess community:")
            click.echo(['20745074', '249601765', '23612012', '917892794953404417',
                        '3161912605', '3392260661', '1617972740', '277594186',
                        '132702118', '482082416'])
            initial_user_list = click.prompt(
                "Provide initial user list", type=str)
            initial_user_list = re.sub("[^\d,]*", '', initial_user_list).split(",")
            click.echo("Initial user list received: ")
            click.echo(initial_user_list)
        elif initial_user_type == 2:
            click.echo("Example: ")
            click.echo("The following are top 10 users calculated "
                       "by intersection ranking of influence one, influence two, "
                       "production, consumption by Core Detector.")
            click.echo("You can use them for practicing Community Expansion.")
            click.echo("ML community:")
            click.echo(
                ['_rockt', 'NandoDF', 'egrefen', 'hardmaru', 'ZoubinGhahrama1',
                 'sarahookr', 'kchonyc', 'JeffDean', 'hugo_larochelle',
                 'shakir_za'])
            click.echo("Chess community:")
            click.echo(['chesscom', 'FIDE_chess', 'STLChessClub', 'chesscom_in',
                        'GrandChessTour', 'fionchetta', 'chess24com',
                        'WorldChessHOF',
                        'TarjeiJS', 'aicfchess'])
            initial_user_list = click.prompt(
                "Provide initial user list", type=str)
            initial_user_list = re.sub('[^a-zA-Z0-9@/_ \n\.]', '',
                                       initial_user_list).split(" ")
            click.echo("Initial user list received: ")
            click.echo(initial_user_list)

        # Currently, we use at most 4 ranking functions
        # InfluenceOneRanker, InfluenceTwoRanker, ProductionUtilityRanker,
        # ConsumptionUtilityRanker
        click.echo("Select Utilities:")
        ranker_list = []
        use_utility = click.prompt("Use Influence One?(y/n)", type=str)
        if use_utility == "y":
            ranker_list.append(InfluenceOneRanker(
                dao_module.get_user_tweet_getter(),
                dao_module.get_user_friend_getter(),
                dao_module.get_ranking_setter()))
        use_utility = click.prompt("Use Influence Two?(y/n)", type=str)
        if use_utility == "y":
            ranker_list.append(InfluenceTwoRanker(
                dao_module.get_user_tweet_getter(),
                dao_module.get_user_friend_getter(),
                dao_module.get_ranking_setter()))
        use_utility = click.prompt("Use Production Utility?(y/n)", type=str)
        if use_utility == "y":
            ranker_list.append(ProductionUtilityRanker(
                dao_module.get_user_tweet_getter(),
                dao_module.get_user_friend_getter(),
                dao_module.get_ranking_setter()))
        use_utility = click.prompt("Use Consumption Utility?(y/n)", type=str)
        if use_utility == "y":
            ranker_list.append(ConsumptionUtilityRanker(
                dao_module.get_user_tweet_getter(),
                dao_module.get_user_friend_getter(),
                dao_module.get_ranking_setter()))
        threshold = click.prompt(
            "Threshold X for utility filtering in decimal"
            "(i.e. top user utility score * 0.2)", type=float)
        top_size = click.prompt(
            "Top X users to measure threshold(i.e. 5)", type=int)
        candidates_size = click.prompt(
            "Number of candidate added each iteration(i.e. 40)", type=int)
        large_account_threshold = click.prompt(
            "Limit X on number of followers in decimal"
            "(i.e. top user follower count * 1.5)\n"
            "If there is no restriction, enter -1", type=float)
        num_of_candidate = click.prompt(
            "Number of potential candidate we check each iteration"
            "(i.e. 200)", type=int)

        core_size = click.prompt(
            "If refine initial users before expansion, "
            "enter number of core users expected in community(i.e. 20)\n"
            "Otherwise, enter -1.", type=int)

    dataset_creator = DatasetCreator(
        file_path,
        dao_module.get_user_getter(),
        process_module.get_user_downloader(),
        dao_module.get_user_tweet_getter(),
        process_module.get_user_tweet_downloader(),
        dao_module.get_user_friend_getter(),
        process_module.get_friend_downloader(),
        ranker_list)

    if core_size != -1:
        core_refiner = CoreRefiner(dao_module.get_user_getter(),
                                   process_module.get_user_downloader(),
                                   dao_module.get_user_tweet_getter(),
                                   process_module.get_user_tweet_downloader(),
                                   dao_module.get_user_friend_getter(),
                                   process_module.get_friend_downloader(),
                                   ranker_list, dataset_creator)
        initial_user_list = core_refiner.refine_core(
            threshold, top_size, candidates_size, large_account_threshold,
            core_size, num_of_candidate, initial_user_list)

    algorithm = CommunityExpansionAlgorithm(
        dao_module.get_user_getter(),
        process_module.get_user_downloader(),
        dao_module.get_user_tweet_getter(),
        process_module.get_user_tweet_downloader(),
        dao_module.get_user_friend_getter(),
        process_module.get_friend_downloader(),
        ranker_list, dataset_creator)

    algorithm.expand_community(
        threshold, top_size, candidates_size,
        large_account_threshold, num_of_candidate, initial_user_list)


def run_community_expansion_graph():
    click.echo("Community Expansion - Create Graph")
    file_path = str(get_project_root()) + "/data/community_expansion/"
    click.echo("Data Path: " + file_path)
    graph_creator = GraphCreator(file_path)
    filename_prefix = click.prompt(
        "filename prefix(core_refine/expansion)", type=str)
    start_iteration = click.prompt("start_iteration", type=int)
    end_iteration = click.prompt("start_iteration", type=int)
    col = click.prompt("utility column in dataset", type=int)
    xlabel = click.prompt("xlabel", type=str)
    ylabel = click.prompt("ylabel", type=str)
    title = click.prompt("title", type=str)

    click.echo("1. Compare different users utility")
    click.echo("2. Compare users utility in different iteration")
    graph_type = click.prompt("Choose graph type", type=int)
    if graph_type == 1:
        graph_creator.create_graph_users(
            filename_prefix, start_iteration, end_iteration, col,
            xlabel, ylabel, title)
    elif graph_type == 2:
        graph_creator.create_graph_iterations(
            filename_prefix, start_iteration, end_iteration, col,
            xlabel, ylabel, title)
    else:
        raise Exception("Invalid input")


@click.command()
def main():
    # Setting up
    DEFAULT_PATH = str(
        get_project_root()) + "/src/scripts/config/create_social_graph_and_cluster_config.yaml"
    injector = Injector.get_injector_from_file(DEFAULT_PATH)
    process_module = injector.get_process_module()
    dao_module = injector.get_dao_module()
    # Run program
    click.echo("====================================================")
    click.echo("                       SNACES                       ")
    click.echo("Social Network Algorithm Contained Experiment System")
    click.echo("====================================================")
    click.echo("Processes:")
    click.echo("1. Download")
    click.echo("2. Raw Tweet Processing")
    click.echo("3. Word Frequency")
    click.echo("4. Social Graph")
    click.echo("5. Clustering")
    click.echo("6. Community Expansion")
    click.echo("7. Community Expansion - Create Graph")

    val = click.prompt("Choose a process")
    if int(val) == 1:
        run_download()
    elif int(val) == 2:
        run_rt_processing()
    elif int(val) == 3:
        run_wf()
    elif int(val) == 4:
        run_social_graph()
    elif int(val) == 5:
        run_clustering()
    elif int(val) == 6:
        run_community_expansion(process_module, dao_module)
    elif int(val) == 7:
        run_community_expansion_graph()
    else:
        raise Exception("Invalid input")


if __name__ == "__main__":
    main()
