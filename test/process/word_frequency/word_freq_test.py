from src.process.word_frequency.word_frequency import *
from src.process.word_frequency.word_freq_mongo_input import *
from src.process.word_frequency.word_freq_mongo_output import *

word_freq = WordFrequency()

# Init input and output daos
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
processed_db = client['ProcessedTweets']
wf_db = client['WordFrequency']

input_dao = WordFrequencyMongoInputDAO()
input_dao.user_processed_tweets_collection = processed_db['UserTweets']
input_dao.user_word_count_vector_collection = wf_db['UserWordCount']

output_dao = WordFrequencyMongoOutputDAO()
output_dao.user_word_count_vector_collection = wf_db['UserWordCount']
output_dao.user_processed_tweets_collection = processed_db['UserTweets']
output_dao.user_word_frequency_vector_collection = wf_db['UserWordFrequency']

# Run tests
word_freq.gen_user_word_count_vector(input_dao, output_dao)
# word_freq.gen_user_word_frequency_vector(input_dao, output_dao)