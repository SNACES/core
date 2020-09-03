from src.process.clustering.affinity_propagation.affinity_propagation import AffinityPropagation
from src.datastore.mongo.word_frequency.word_freq_mongo_get import WordFrequencyMongoGetDAO
from src.datastore.mongo.cluster.affinity_propagation.aff_prop_mongo_set import AffinityPropagationMongoSetDAO
# from src.process.clustering.clustering_lib import cluster_relative_frequency

aff_prop = AffinityPropagation()

# Init input and output daos
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
wf_db = client['WordFrequency-Test']
cluster_db = client['Cluster-Test']

wf_get = WordFrequencyMongoGetDAO()
wf_get.relative_user_word_frequency_vector_collection = wf_db['RelativeUserWordFrequency']

aff_prop_set = AffinityPropagationMongoSetDAO()
aff_prop_set.clusters_collection = cluster_db['AffinityPropagation']

# Run tests
clusters = aff_prop.gen_clusters(wf_get, aff_prop_set)
