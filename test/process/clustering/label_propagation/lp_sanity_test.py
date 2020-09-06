from src.process.download.twitter_downloader import TwitterFriendsDownloader
from src.datastore.tweepy.tweepy_get import TweepyGetDAO
from src.process.clustering.label_propagation.label_propagation import LabelPropagation
from src.process.social_graph.social_graph import SocialGraph
from src.datastore.mongo.user_friend.user_friends_mongo_set import UserFriendsMongoSetDAO
from src.datastore.mongo.user_friend.user_friends_mongo_get import UserFriendsMongoGetDAO
from src.datastore.mongo.social_graph.social_graph_mongo_get import SocialGraphMongoGetDAO
from src.datastore.mongo.social_graph.social_graph_mongo_set import SocialGraphMongoSetDAO
from src.datastore.mongo.cluster.label_propagation.label_prop_mongo_set import LabelPropagationMongoSetDAO

# Init input and output daos
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['LabelPropagation-Test']

tweepy_getter = TweepyGetDAO()

user_friends_setter = UserFriendsMongoSetDAO()
user_friends_setter.user_friends_by_name_collection = db['UserFriends']

user_friends_getter = UserFriendsMongoGetDAO()
user_friends_getter.user_friends_by_name_collection = db['UserFriends']

social_graph_setter = SocialGraphMongoSetDAO()
social_graph_setter.user_friends_graph_collection = db['UserFriendsGraph']

social_graph_getter = SocialGraphMongoGetDAO()
social_graph_getter.user_friends_graph_collection = db['UserFriendsGraph']

label_prop_cluster_setter = LabelPropagationMongoSetDAO()
label_prop_cluster_setter.clusters_collection = db['LabelPropClusters']

# Run tests
user = "hardmaru"
# Download local community for user
friends_downloader = TwitterFriendsDownloader()
friends_downloader.gen_user_local_neighborhood(user, tweepy_getter, user_friends_getter, user_friends_setter)

# # Generate User Friends Graph
social_graph_downloader = SocialGraph()
social_graph_downloader.gen_user_friends_graph(user, user_friends_getter, social_graph_setter)

# # Run label propagation to get clusters
lab_prop = LabelPropagation()
lab_prop.gen_clusters(user, social_graph_getter, label_prop_cluster_setter)