from typing import Union, List
from mongoDAO import MongoDAO
import collections
import datetime

# TODO: implement lazy mode: this makes sure that accurate wc and wf vectors are generated
# to do this, need to keep track of which processed tweets have already had their words counted
class WordFrequencyMongoInput(MongoDAO, InputDAO):
    def __init__(self):
        super().__init__()
        self.global_processed_tweets_collection = None
        self.user_processed_tweets_collection = None
        self.global_word_count_vector_collection = None
        self.user_word_count_vector_collection = None
        self.global_word_frequency_vector_collection = None
        self.user_word_frequency_vector_collection = None
    
    def get_global_tweet_words(self, lazy=True):
        """
        Return a list of all words from tweets in the global processed tweets collection.
        Input database doc format: {'tweet_words': [str]}
        """

        global_tweet_words = []
        if lazy:
            processed_tweet_list = self.global_processed_tweets_collection.find({
                'is_counted': False
            }, {
                'is_counted': "null"
            })
        else:
            processed_tweet_list = self.global_processed_tweets_collection.find()

        # Run through tweets in collection and collect words from tweets
        for tweet_doc in processed_tweet_list:
            global_tweet_words.extend(tweet_doc['tweet_words'])

        return global_tweet_words

    def get_user_tweet_words(self, lazy=True):
        """
        Return for each user a list of all words from tweets in the user processed tweets collection.
        Input database doc format: {'user': str, 'processed_tweets' [{'tweet_words': [str]}]}
        Return format: {user: [words]}
        """

        user_to_tweet_words = {}

        if lazy:
            user_tweet_doc_list = self.user_processed_tweets_collection.find({
                'processed_tweets': [{'is_processed': False}]
            },
            {
                'processed_tweets': [{'is_processed': "null"}]
            })
        else:
            user_tweet_doc_list = self.user_processed_tweets_collection.find()

        # Run through tweets in collection and collect words from tweets
        for user_doc in self.user_processed_tweets_collection.find():
            user = user_doc['user']
            tweet_words = []
            
            for processed_tweet in user_doc['processed_tweets']:
                tweet_words.extend(processed_tweet['tweet_words'])

            user_to_tweet_words[user] = tweet_words

        return user_to_tweet_words

    def get_global_word_count_vector(self):
        """
        Return the global word count vector.
        Format: {word: word count}
        """
        
        # According to our database format, the global word count vector collection
        # only contains one doc
        global_word_count_vector = self.global_word_count_vector_collection.find_one()

        return global_word_count_vector

    def get_user_word_count_vector(self):
        """
        Return the user word count vector
        Format: {user: {word: word count}}
        """
        
        user_word_count_vector = {}
        
        for user_doc in self.user_word_count_vector_collection.find():
            user = user_doc['user']
            word_count_vector = user_doc['word_count_vector']
            user_word_count_vector[user] = word_count_vector

        return user_word_count_vector

    def get_global_word_frequency_vector(self):
        """
        Return the global word frequency vector.
        Format: {word: word frequency}
        """
        
        # According to our database format, the global word frequency vector collection
        # only contains one doc
        global_word_frequency_vector = self.global_word_frequency_vector_collection.find_one()

        return global_word_frequency_vector

    def get_user_word_frequency_vector(self):
        """
        Return the user word frequency vector.
        Format: {user: {word: word frequency}}
        """
        
        user_word_frequency_vector = {}
        
        for user_doc in self.user_word_frequency_vector_collection.find():
            user = user_doc['user']
            word_frequency_vector = user_doc['word_frequency_vector']
            user_word_frequency_vector[user] = word_frequency_vector

        return user_word_frequency_vector



















# def generate_global_word_frequency_vector(self, date: datetime, input_collection_name, output_collection_name):
    #     # TODO: finish fixing this
        
    #     daily_processed_tweet_text = self.input_DAOs[input_collection_name].get_processed_tweet
        
    #     words = []
    #     for processed_tweet in daily_processed_tweet_text:
    #         words.extend(processed_tweet['processed-text-list'])
        
    #     word_freq_vector = self._get_word_frequency_vector(words)
    #     if word_freq_vector:
    #         self.output_DAOs[output_collection_name].store_daily_global_word_frequency_vector

    # def generate_user_word_frequency_vector(self, date: datetime, user, output_collection_name, date_input_config=None, output_config=None):
    #     # TODO: handle default value for date_input_config
    #     input_name = date_input_config['collection-name']
    #     if input_name not in self.input_DAOs:
    #         # dynamically create new DAO
    #         self.input_DAOs[input_name] = self.DAO_factory.create_DAO_from_config("input", date_input_config)
    #     # TODO: dates issue
    #     collection = self.input_DAOs[input_name].read({ "id": user, "start_date": date })
    #     user_daily_tweet_text = [tweet['text'] for tweets_doc in collection for tweet in tweets_doc['tweets']]

    #     # process 
    #     words = []
    #     for text in user_daily_tweet_text:
    #         processed_text_list = self._process_tweet_text(text)
    #         words.extend(processed_text_list)
    #     # print(words)
        
    #     word_freq_vector = self._get_word_frequency_vector(words)
    #     # print(word_freq_vector)
    #     if word_freq_vector:
    #         word_freq_vector_doc = {
    #             "User": user,
    #             "Date": date,
    #             "WordFreqVector": word_freq_vector
    #         }

    #         # output_collection_name generated based on the date
    #         # output_collection_name = "UserWordFrequency"
    #         output_config['collection-name'] = output_collection_name
    #         if output_collection_name not in self.output_DAOs:
    #             # dynamically create new DAO
    #             self.output_DAOs[output_collection_name] = self.DAO_factory.create_DAO_from_config("output", output_config) 
    #         self.output_DAOs[output_collection_name].create(word_freq_vector_doc)


    # def generate_relative_user_word_frequency_vector(self, start_date: datetime, 
    #             end_date: datetime, user, user_word_freq_config={}, global_word_freq_config=None, output_collection_name="", output_config=None):
    #     # get user_word_frequency vectors for timeframe
    #         # combine the counters to get megacounter
    #     input_name = global_word_freq_config['collection-name']
    #     if input_name not in self.input_DAOs:
    #         # dynamically create new DAO
    #         self.input_DAOs[input_name] = self.DAO_factory.create_DAO_from_config("input", global_word_freq_config)

    #     daily_global_vectors = []
    #     for date in daterange(start_date, end_date): # TODO: modulaize this for global and user
    #         # print(date)
    #         # date = date.strftime("%Y-%m-%d")
    #         query = self.input_DAOs[input_name].read({"Date": date})
    #         daily_vectors = [collections.Counter(daily_vector_doc["WordFreqVector"]) for daily_vector_doc in query]
    #         daily_global_vectors.extend(daily_vectors)
    #     # print(daily_global_vectors)
    #     timeframe_global_word_freq = sum(daily_global_vectors, collections.Counter())
        
    #     # get global word frequency vectors for time frame
    #         # combine the counters to get megacounter
    #     input_name = user_word_freq_config['collection-name']
    #     if input_name not in self.input_DAOs:
    #         # dynamically create new DAO
    #         self.input_DAOs[input_name] = self.DAO_factory.create_DAO_from_config("input", user_word_freq_config)

    #     daily_user_vectors = []
    #     for date in daterange(start_date, end_date):
    #         query = self.input_DAOs[input_name].read({"User": user, "Date": date})
    #         daily_vectors = [collections.Counter(daily_vector_doc["WordFreqVector"]) for daily_vector_doc in query]
    #         daily_user_vectors.extend(daily_vectors)
    #     timeframe_user_word_freq = sum(daily_user_vectors, collections.Counter())
    #     # print(timeframe_user_word_freq)
    #     # print(timeframe_global_word_freq)
    #     # for each word in user vector
    #         # if in global
    #             # get relative
    #         # else 
    #             # get 
    #     user_words_not_in_global = []
    #     relative_word_freq = {}
    #     for word in timeframe_user_word_freq:
    #         user_word_count = timeframe_user_word_freq[word]
    #         if user_word_count >= 3:
    #             if word in timeframe_global_word_freq:
    #                 global_word_count = timeframe_global_word_freq[word]
    #                 relative_word_freq[word] = user_word_count / global_word_count
    #             else:
    #                 user_words_not_in_global.append(word)

    #     # store  
    #     output_doc = {
    #         "User": user,
    #         "StartDate": start_date,
    #         "EndDate": end_date,
    #         "RelativeWordFrequency": relative_word_freq,
    #         "UserWordsNotInGlobal": user_words_not_in_global
    #     }
    #     # print(output_doc)
    #     output_config["collection-name"] = output_collection_name
    #     if output_collection_name not in self.output_DAOs:
    #         # dynamically create new DAO
    #         self.output_DAOs[output_collection_name] = self.DAO_factory.create_DAO_from_config("output", output_config) 
    #     self.output_DAOs[output_collection_name].create(output_doc)
        

# TODO: maybe make this a general helper
# def daterange(start_date, end_date):
#     for n in range(int ((end_date - start_date).days)):
#         yield start_date + datetime.timedelta(n)    