from typing import Union, List
from collections import Counter

class WordFrequencyMongoSetDAO():
    """
    A class that stores data collection into MongoDB.

    @private 
        global_word_count_vector_collection: global word count to be stored into MongoBD
        user_word_count_vector_collection: user word count to be stored into MongoDB
        global_word_frequency_vector_collection: global word frequency to be stored into MongoDB
        user_word_frequency_vector_collection: global word frequency of specific users to be stored into MongoDB
        relative_user_word_frequency_vector_collection: relative word frequency of specific users to be stored into MongoDB
    """
    # Important to distinguish between new entry and update
    def __init__(self):
        """
        Initilize a new WordFrequencyMongoSetDAO class.
        """
        self.global_word_count_vector_collection = None
        self.user_word_count_vector_collection = None
        self.global_word_frequency_vector_collection = None
        self.user_word_frequency_vector_collection = None
        self.relative_user_word_frequency_vector_collection = None

    def store_global_word_count_vector(self, global_wc_vector):
        """
        Store global word count vector in descending order.

        @param global_wc_vector: global word vector to be stored
        """

        # Check whether an existing entry exists, update if so
        existing_global_wc_vector = self.global_word_count_vector_collection.find_one({}, {'_id': 0})
        if existing_global_wc_vector:
            existing_global_wc_vector = Counter(existing_global_wc_vector)
            global_wc_vector = Counter(global_wc_vector)
            updated_global_wc_vector = existing_global_wc_vector + global_wc_vector
            updated_global_wc_vector = {word:wc for word, wc in updated_global_wc_vector.most_common()}
            self.global_word_count_vector_collection.replace_one({}, updated_global_wc_vector)
        else:
            # Add global_wc_vector as a new entry
            global_wc_vector = {word:wc for word, wc in global_wc_vector.most_common()}
            self.global_word_count_vector_collection.insert_one(global_wc_vector)
    
    def store_user_word_count_vector(self, user_wc_vector):
        """
        Store user word count vector in descending order.

        @user_ec_vector: user word vector to be stored
        """

        for user in user_wc_vector:
            wc_vector = Counter(user_wc_vector[user])

            user_doc = self.user_word_count_vector_collection.find_one({
                'user': user
            })
            if user_doc:
                # Update
                existing_wc_vector = Counter(user_doc['word_count_vector'])
                updated_wc_vector = existing_wc_vector + wc_vector
                updated_wc_vector = {word:wc for word, wc in updated_wc_vector.most_common()}
                self.user_word_count_vector_collection.replace_one({
                    'user': user
                }, {
                    'user': user,
                    'word_count_vector': updated_wc_vector 
                })
            else:
                # Add new entry
                wc_vector = {word:wc for word, wc in wc_vector.most_common()}
                self.user_word_count_vector_collection.insert_one({
                    'user': user,
                    'word_count_vector': wc_vector 
                })

    def store_global_word_frequency_vector(self, global_wf_vector):
        """
        Store global word frequency vector in descending order.

        @param global_wf_vector: global word frequency vector to be stored
        """

        global_wf_vector = Counter(global_wf_vector)
        global_wf_vector = {word:wf for word, wf in global_wf_vector.most_common()}

        # Check whether an existing entry exists, update if so
        existing_global_wf_vector = self.global_word_frequency_vector_collection.find_one({}, {'_id': 0})
        if existing_global_wf_vector:
            global_wf_vector = Counter(global_wf_vector)
            self.global_word_frequency_vector_collection.replace_one({}, global_wf_vector)
        else:
            # Add global_wf_vector as a new entry
            self.global_word_frequency_vector_collection.insert_one(global_wf_vector)
    
    def store_user_word_frequency_vector(self, user_wf_vector):
        """
        Store user word frequency vector in descending order.

        @param user_wf_vector: word frequency vector of specific users to be stored
        """

        for user in user_wf_vector:
            wf_vector = Counter(user_wf_vector[user])
            wf_vector = {word:wf for word, wf in wf_vector.most_common()}

            user_doc = self.user_word_frequency_vector_collection.find_one({
                'user': user
            })
            if user_doc:
                # Update
                self.user_word_frequency_vector_collection.replace_one({
                    'user': user
                }, {
                    'user': user,
                    'word_frequency_vector': wf_vector
                })
            else:
                # Add new entry
                self.user_word_frequency_vector_collection.insert_one({
                    'user': user,
                    'word_frequency_vector': wf_vector 
                })
        
    def store_relative_user_word_frequency_vector(self, relative_user_wf_vector):
        """
        Store relative user word frequency vector in descending order.

        @param relative_user_wf_vector: list of relative word frequency of specific users
        """

        for user in relative_user_wf_vector:
            relative_wf_vector = Counter(relative_user_wf_vector[user])
            relative_wf_vector = {word:rwf for word, rwf in relative_wf_vector.most_common()}

            user_doc = self.relative_user_word_frequency_vector_collection.find_one({
                'user': user
            })
            if user_doc:
                # Update
                self.relative_user_word_frequency_vector_collection.replace_one({
                    'user': user
                }, {
                    'user': user,
                    'relative_word_frequency_vector': relative_wf_vector 
                })
            else:
                # Add new entry
                self.relative_user_word_frequency_vector_collection.insert_one({
                    'user': user,
                    'relative_word_frequency_vector': relative_wf_vector 
                })
