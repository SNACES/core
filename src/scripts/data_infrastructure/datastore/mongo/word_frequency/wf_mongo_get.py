import collections
import datetime
from typing import Union, List

# lazy mode: this makes sure that accurate wc and wf vectors are generated
# to do this, need to keep track of which processed tweets have already had their words counted
class WordFrequencyMongoGetDAO():
    """
    A class that gets data collection from MongoDB.

    @private 
        global_word_count_vector_collection: global word count from MongoBD
        user_word_count_vector_collection: user word count from MongoDB
        global_word_frequency_vector_collection: global word frequency from MongoDB
        user_word_frequency_vector_collection: global word frequency of specific users
        relative_user_word_frequency_vector_collection: relative word frequency of specific users
    """
    def __init__(self):
        """
        Initialize a new WordFrequencyMongoGetDAO class.
        """
        self.global_word_count_vector_collection = None
        self.user_word_count_vector_collection = None
        self.global_word_frequency_vector_collection = None
        self.user_word_frequency_vector_collection = None
        self.relative_user_word_frequency_vector_collection = None

    def get_global_word_count_vector(self):
        """
        Generate the global word count vector of format: {word: word count}

        @return: the global word count vector
        """
        
        # According to our database format, the global word count vector collection
        # only contains one doc
        global_word_count_vector = self.global_word_count_vector_collection.find_one({}, {'_id': 0})

        return global_word_count_vector

    def get_user_word_count_vector(self):
        """
        Generate the user word count vector of the format: {user: {word: word count}}.

        @return: user word count vector of the users
        """
        
        user_word_count_vector = {}
        
        for user_doc in self.user_word_count_vector_collection.find():
            user = user_doc['user']
            word_count_vector = user_doc['word_count_vector']
            user_word_count_vector[user] = word_count_vector

        return user_word_count_vector

    def get_global_word_frequency_vector(self):
        """
        Generate the global word frequency vector of the format: {word: word frequency}.

        @return: global word frequency vector
        """
        
        # According to our database format, the global word frequency vector collection
        # only contains one doc
        global_word_frequency_vector = self.global_word_frequency_vector_collection.find_one({}, {'_id': 0})

        return global_word_frequency_vector

    def get_user_word_frequency_vector(self):
        """
        Generate the user word frequency vector of the format: {user: {word: word frequency}}.

        @return: word frequency vector of users
        """
        
        user_word_frequency_vector = {}
        
        for user_doc in self.user_word_frequency_vector_collection.find():
            user = user_doc['user']
            word_frequency_vector = user_doc['word_frequency_vector']
            user_word_frequency_vector[user] = word_frequency_vector

        return user_word_frequency_vector
    
    def get_relative_user_word_frequency_vector(self):
        """
        Generate the relative user word frequency vector fo the format: {user: {word: relative word frequency}}
        
        @return: relative word frequency vector of the users
        """
        
        relative_user_word_frequency_vector = {}
        
        for user_doc in self.relative_user_word_frequency_vector_collection.find():
            user = user_doc['user']
            relative_word_frequency_vector = user_doc['relative_word_frequency_vector']
            relative_user_word_frequency_vector[user] = relative_word_frequency_vector

        return relative_user_word_frequency_vector