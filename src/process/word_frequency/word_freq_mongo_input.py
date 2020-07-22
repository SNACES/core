import collections
import datetime
from typing import Union, List

# TODO: implement lazy mode: this makes sure that accurate wc and wf vectors are generated
# to do this, need to keep track of which processed tweets have already had their words counted
class WordFrequencyMongoInputDAO():
    def __init__(self):
        self.global_processed_tweets_collection = None
        self.user_processed_tweets_collection = None
        self.global_word_count_vector_collection = None
        self.user_word_count_vector_collection = None
        self.global_word_frequency_vector_collection = None
        self.user_word_frequency_vector_collection = None
        self.relative_user_word_frequency_vector_collection = None
    
    def get_global_tweet_words(self, lazy=True):
        """
        Return a list of all words from tweets in the global processed tweets collection.
        Input database doc format: {'tweet_words': [str]}
        """

        global_tweet_words = []
        if lazy:
            processed_tweet_list = self.global_processed_tweets_collection.find({
                'is_counted': {'$ne': True}
            })
        else:
            processed_tweet_list = self.global_processed_tweets_collection.find()

        # Run through tweets in collection and collect words from tweets
        for tweet_doc in processed_tweet_list:
            global_tweet_words.extend(tweet_doc['tweet_words'])

        return global_tweet_words

    def get_user_tweet_words(self, lazy=False): # TODO: change back to true once lazy mode fixed
        """
        Return for each user a list of all words from tweets in the user processed tweets collection.
        Input database doc format: {'user': str, 'processed_tweets' [{'tweet_words': [str]}]}
        Return format: {user: [words]}
        """

        user_to_tweet_words = {}

        if lazy:
            # user_tweet_doc_list = self.user_processed_tweets_collection.find({
            #     'processed_tweets': [{'is_processed': False}]
            # },
            # {
            #     'processed_tweets': [{'is_processed': "null"}]
            # })
            user_tweet_doc_list = self.user_processed_tweets_collection.find({
                'processed_tweets': {'is_counted': False}
            })
        else:
            user_tweet_doc_list = self.user_processed_tweets_collection.find()

        # Run through tweets in collection and collect words from tweets
        for user_doc in user_tweet_doc_list:
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
        global_word_count_vector = self.global_word_count_vector_collection.find_one({}, {'_id': 0})

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
    
    def get_relative_user_word_frequency_vector(self):
        """
        Return the relative user word frequency vector.
        Format: {user: {word: relative word frequency}}
        """
        
        relative_user_word_frequency_vector = {}
        
        for user_doc in self.relative_user_word_frequency_vector_collection.find():
            user = user_doc['user']
            relative_word_frequency_vector = user_doc['relative_word_frequency_vector']
            relative_user_word_frequency_vector[user] = relative_word_frequency_vector

        return relative_user_word_frequency_vector