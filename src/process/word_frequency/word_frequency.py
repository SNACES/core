from typing import Union, List
from collections import Counter
from copy import copy

class WordFrequency():
    def gen_global_word_count_vector(self, input_dao, output_dao):
        """
        Assume that the input dao contains tweets.
        The common format is a list of words from the tweets.
        The global word count vector format is {word: num_times_used}
        Return and store the global word count vector. 
        """
        
        tweet_word_list = input_dao.get_global_tweet_words()
        global_wc_vector = self._process_global_word_count_vector(tweet_word_list)
        output_dao.store_global_word_count_vector(global_wc_vector)
        output_dao.update_global_processed_tweet_state()

        return global_wc_vector
    
    def gen_user_word_count_vector(self, input_dao, output_dao):
        """
        Assume that the input dao contains tweets for users.
        The common format is a {user: [words from user's tweets]}.
        The user word count vector format is {user: {word: num_times_used}}
        Return and store the user word count vector.
        """
        
        user_to_tweet_word_list = input_dao.get_user_tweet_words()
        user_wc_vector = self._process_user_word_count_vector(user_to_tweet_word_list)
        output_dao.store_user_word_count_vector(user_wc_vector)
        output_dao.update_user_processed_tweet_state()

        return user_wc_vector

    def gen_global_word_frequency_vector(self, input_dao, output_dao):
        """
        Assume that the input dao contains the global word count vector.
        The common format is {word: num_times_used}.
        The global word frequency vector format is {word: gwf}
        Return and store the global word frequency vector. 
        """

        global_wc_vector = input_dao.get_global_word_count_vector()
        global_wf_vector = self._process_global_word_frequency_vector(global_wc_vector)
        output_dao.store_global_word_frequency_vector(global_wf_vector)

        return global_wf_vector

    def gen_user_word_frequency_vector(self, input_dao, output_dao):
        """
        Assume that the input dao contains the user word count vector.
        The common format is {user: {word: num_times_used}}.
        The global word frequency vector format is {user: {word: uwf}}
        Return and store the user word frequency vector.
        """

        user_wc_vector = input_dao.get_user_word_count_vector()
        user_wf_vector = self._process_user_word_frequency_vector(user_wc_vector)
        output_dao.store_user_word_frequency_vector(user_wf_vector)

        return user_wf_vector

    def gen_relative_user_word_frequency_vector(self, input_dao, output_dao):
        """
        Assume that the input dao contains the global and user word frequency vectors.
        The common format is the global and user word frequency vectors specified previously.
        Return and store the relative user word frequency vector.
        """

        global_wf_vector = input_dao.get_global_word_frequency_vector()
        user_wf_vector = input_dao.get_user_word_frequency_vector()
        user_to_wcv = input_dao.get_user_word_count_vector()
        relative_user_wf_vector = self._process_relative_user_word_frequency_vector(global_wf_vector,
                                                                                    user_wf_vector,
                                                                                    user_to_wcv)
        output_dao.store_relative_user_word_frequency_vector(relative_user_wf_vector)
        
        return relative_user_wf_vector

    def _process_global_word_count_vector(self, words):
        word_freq_vector = Counter()
        
        for word in words:
            word_freq_vector[word] += 1

        return word_freq_vector

    def _process_user_word_count_vector(self, user_to_tweet_word_list):
        return {user:self._process_global_word_count_vector(user_to_tweet_word_list[user]) 
                for user in user_to_tweet_word_list}
    
    def _process_global_word_frequency_vector(self, global_wc_vector):
        """
        gwf = global_count/total_global_count
        """

        total_global_count = sum([global_wc_vector[word] for word in global_wc_vector])

        for word in global_wc_vector:
            global_wc_vector[word] /= float(total_global_count)

        return global_wc_vector

    def _process_user_word_frequency_vector(self, user_wc_vector):
        """
        uwf = user_count/total_user_count
        """
        
        return {user:self._process_global_word_frequency_vector(user_wc_vector[user])
                for user in user_wc_vector}
    
    def _process_relative_user_word_frequency_vector(self, global_wf_vector, user_wf_vector, user_to_wcv):
        """
        rwf = uwf/gwf
        If a user word does not appear in the global count, then global_count = local_count.
        """

        relative_uwf_vector = {}
        local_community_cache = {}

        for user in user_wf_vector:
            relative_wf_vector = copy(user_wf_vector[user])
            
            for word in relative_wf_vector:
                global_count = global_wf_vector[word] if word in global_wf_vector else 0
                
                if global_count == 0:
                    # we can cache local community count
                    if word not in local_community_cache:
                        local_community_count = 0
                        for user_ in user_to_wcv:
                            u_word_counter = user_to_wcv[user_]
                            if word in u_word_counter:
                                local_community_count += u_word_counter[word]
                        local_community_cache[word] = local_community_count
                    else:
                        local_community_count = local_community_cache[word]
                    global_count = local_community_count
                
                relative_wf_vector[word] /= float(global_count)
            
            relative_uwf_vector[user] = relative_wf_vector

        return relative_uwf_vector


    