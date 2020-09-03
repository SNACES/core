from src.process.word_frequency.word_frequency import WordFrequency
from src.datastore.mongo.processed_tweet.processed_tweet_mongo_get import ProcessedTweetMongoGetDAO
from src.datastore.mongo.processed_tweet.processed_tweet_mongo_set import ProcessedTweetMongoSetDAO
from src.datastore.mongo.word_frequency.word_freq_mongo_get import WordFrequencyMongoGetDAO
from src.datastore.mongo.word_frequency.word_freq_mongo_set import WordFrequencyMongoSetDAO

word_freq = WordFrequency()

# Init input and output daos
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
processed_db = client['ProcessedTweets-Test']
wf_db = client['WordFrequency-Test']

processed_tweet_get = ProcessedTweetMongoGetDAO()
processed_tweet_set = ProcessedTweetMongoSetDAO()
wf_get = WordFrequencyMongoGetDAO()
wf_set = WordFrequencyMongoSetDAO()

processed_tweet_set.user_processed_tweets_collection = processed_db['UserTweets']
processed_tweet_set.global_processed_tweets_collection = processed_db['GlobalTweets']

processed_tweet_get.global_processed_tweets_collection = processed_db['GlobalTweets']
wf_get.global_word_count_vector_collection = wf_db['GlobalWordCount']
wf_get.global_word_frequency_vector_collection = wf_db['GlobalWordFrequency']

processed_tweet_get.user_processed_tweets_collection = processed_db['UserTweets']
wf_get.user_word_count_vector_collection = wf_db['UserWordCount']
wf_get.user_word_frequency_vector_collection = wf_db['UserWordFrequency']

wf_get.relative_user_word_frequency_vector_collection = wf_db['RelativeUserWordFrequency']

wf_set.global_word_count_vector_collection = wf_db['GlobalWordCount']
wf_set.global_processed_tweets_collection = processed_db['GlobalTweets']
wf_set.global_word_frequency_vector_collection = wf_db['GlobalWordFrequency']

wf_set.user_word_count_vector_collection = wf_db['UserWordCount']
wf_set.user_processed_tweets_collection = processed_db['UserTweets']
wf_set.user_word_frequency_vector_collection = wf_db['UserWordFrequency']

wf_set.relative_user_word_frequency_vector_collection = wf_db['RelativeUserWordFrequency']

# Run tests
# word_freq.gen_global_word_count_vector(processed_tweet_get, processed_tweet_set, wf_set)
# word_freq.gen_global_word_frequency_vector(wf_get, wf_set)

# word_freq.gen_user_word_count_vector(processed_tweet_get, processed_tweet_set, wf_set)
# word_freq.gen_user_word_frequency_vector(wf_get, wf_set)

# word_freq.gen_relative_user_word_frequency_vector(wf_get, wf_set)
