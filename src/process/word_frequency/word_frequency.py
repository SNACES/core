from typing import Union, List
from collections import Counter
from copy import copy

class WordFrequency():
    """
    A class that contains all data processing functions involved in Word frequency.
    """
    def gen_global_word_count_vector(self, processed_tweet_getter, processed_tweet_setter, wf_setter):
        """
        Generate the global word count vector.
        Assume that the input dao contains tweets.
        The common format is a list of words from the tweets.

        @param processed_tweet_getter: a processed tweet mongo GetDAO
        @param processed_tweet_setter: a processed tweet mongo SetDAO
        @param wf_setter: a Word Frequency SetDAO
        @return: store the global word count vector format, with format: {word: num_times_used}
        """
        
        tweet_word_list = processed_tweet_getter.get_global_tweet_words()
        global_wc_vector = self._process_global_word_count_vector(tweet_word_list)
        wf_setter.store_global_word_count_vector(global_wc_vector)
        processed_tweet_setter.update_global_processed_tweet_state()

        return global_wc_vector
    
    def gen_user_word_count_vector(self, processed_tweet_getter, processed_tweet_setter, wf_setter):
        """
        Generate the word count vector of specific user.
        Assume that the input dao contains tweets for users.
        The common format is a {user: [words from user's tweets]}.

        @param processed_tweet_getter: a processed tweet mongo GetDAO
        @param processed_tweet_setter: a processed tweet mongo SetDAO
        @param wf_setter: a Word Frequency SetDAO
        @return: store the user's global word count vector format, with format: user: {word: num_times_used}}
        """
        
        user_to_tweet_word_list = processed_tweet_getter.get_user_tweet_words()
        user_wc_vector = self._process_user_word_count_vector(user_to_tweet_word_list)
        wf_setter.store_user_word_count_vector(user_wc_vector)
        processed_tweet_setter.update_user_processed_tweet_state()

        return user_wc_vector

    def gen_global_word_frequency_vector(self, wf_getter, wf_setter):
        """
        Generate the global word frequency
        Assume that the input dao contains the global word count vector.
        The common format is {word: num_times_used}.

        @param wf_getter: a Word Frequency GetDAO
        @param wf_setter: a Word Frequency SetDAO
        @return: store and return the global word frequency vector, with the format {word: gwf}. 
        """

        global_wc_vector = wf_getter.get_global_word_count_vector()
        global_wf_vector = self._process_global_word_frequency_vector(global_wc_vector)
        wf_setter.store_global_word_frequency_vector(global_wf_vector)

        return global_wf_vector

    def gen_user_word_frequency_vector(self, wf_getter, wf_setter):
        """
        Generate the word frequency of a specific user.
        Assume that the input dao contains the user word count vector.
        The common format is {user: {word: num_times_used}}.

        @param wf_getter: a Word Frequency GetDAO
        @param wf_setter: a Word Frequency SetDAO
        @return: store and return the user's global word frequency vector, with the format {user: {word: uwf}}. 
        """

        user_wc_vector = wf_getter.get_user_word_count_vector()
        user_wf_vector = self._process_user_word_frequency_vector(user_wc_vector)
        wf_setter.store_user_word_frequency_vector(user_wf_vector)

        return user_wf_vector

    def gen_relative_user_word_frequency_vector(self, wf_getter, wf_setter):
        """
        Generate the relative word frequenct of a specific user.
        Assume that the input dao contains the global and user word frequency vectors.
        The common format is the global and user word frequency vectors specified previously.

        @param wf_getter: a Word Frequency GetDAO
        @param wf_setter: a Word Frequency SetDAO
        @return: store and return the user's relative global word frequency vector, 
        with the format {user: {word: ruwf}}.
        """

        global_wf_vector = wf_getter.get_global_word_frequency_vector()
        user_wf_vector = wf_getter.get_user_word_frequency_vector()
        user_to_wcv = wf_getter.get_user_word_count_vector()
        relative_user_wf_vector = self._process_relative_user_word_frequency_vector(global_wf_vector,
                                                                                    user_wf_vector,
                                                                                    user_to_wcv)
        wf_setter.store_relative_user_word_frequency_vector(relative_user_wf_vector)
        
        return relative_user_wf_vector

    def _process_global_word_count_vector(self, words):
        """
        Count the number of each word in the word list.

        @param words: the word list to be count
        @return: the number of each word in the words
        """
        word_freq_vector = Counter()
        
        for word in words:
            word_freq_vector[word] += 1

        return word_freq_vector

    def _process_user_word_count_vector(self, user_to_tweet_word_list):
        """
        Count the number of words of specific users.

        @param user_to_tweet_word_list: a list containing word list for each user.
        @return: the number of words of specific users.
        """
        return {user:self._process_global_word_count_vector(user_to_tweet_word_list[user]) 
                for user in user_to_tweet_word_list}
    
    def _process_global_word_frequency_vector(self, global_wc_vector):
        """
        Generate the word frequency by gwf = global_count/total_global_count.

        @param global_wc_vector: the generated global word vector
        @return: the word frequency of the global word vector
        """

        total_global_count = sum([global_wc_vector[word] for word in global_wc_vector])

        for word in global_wc_vector:
            global_wc_vector[word] /= float(total_global_count)

        return global_wc_vector

    def _process_user_word_frequency_vector(self, user_wc_vector):
        """
        Generate the word frequency of the user by uwf = user_count/total_user_count

        @param user_wc_vector: the generated user word vector
        @return: the word frequency of the user word vector
        """
        
        return {user:self._process_global_word_frequency_vector(user_wc_vector[user])
                for user in user_wc_vector}
    
    def _process_relative_user_word_frequency_vector(self, global_wf_vector, user_wf_vector, user_to_wcv):
        """
        Generate the relative word frequency of the users by rwf = uwf/gwf
        If a user word does not appear in the global count, then global_count = local_count.

        @param global_wf_vector: global word frequency vector
        @param user_wf_vector: global word frequency vector of the users
        @param user_to_wcv: global count vector of the users
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


    