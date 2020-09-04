from src.process.clustering.MUISI.standard.muisi import MUISI, MUISIConfig
from src.datastore.mongo.word_frequency.word_freq_mongo_get import WordFrequencyMongoGetDAO
from src.datastore.mongo.cluster.MUISI.standard.muisi_mongo_set import MUISIMongoSetDAO

# Init input and output daos
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
wf_db = client['WordFrequency-Test']
muisi_db = client['MUISI-Test']

wf_getter = WordFrequencyMongoGetDAO()
wf_getter.user_word_frequency_vector_collection = wf_db['UserWordFrequency']
wf_getter.relative_user_word_frequency_vector_collection = wf_db['RelativeUserWordFrequency'] 

muisi_cluster_setter = MUISIMongoSetDAO()
muisi_cluster_setter.muisi_cluster_collection = muisi_db['MUISIClusters']

# Run tests
intersection_min = 2
popularity = 0.3
threshold = 0.5
user_count = 5
item_count = 5
count = 5
is_only_popularity = True
muisi_config = MUISIConfig(intersection_min, popularity, threshold, user_count, 
                 item_count, count, is_only_popularity)

muisi = MUISI()
muisi.gen_clusters(muisi_config, wf_getter, muisi_cluster_setter)
