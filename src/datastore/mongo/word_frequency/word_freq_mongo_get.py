import collections
import datetime
from typing import Union, List

# lazy mode: this makes sure that accurate wc and wf vectors are generated
# to do this, need to keep track of which processed tweets have already had their words counted
class WordFrequencyMongoGetDAO():
    def __init__(self):
        self.global_word_count_vector_collection = None
        self.user_word_count_vector_collection = None
        self.global_word_frequency_vector_collection = None
        self.user_word_frequency_vector_collection = None
        self.relative_user_word_frequency_vector_collection = None

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
        global_word_frequency_vector = self.global_word_frequency_vector_collection.find_one({}, {'_id': 0})

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