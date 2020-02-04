import sys
sys.path.append('../General')
sys.path.append('../General/Concrete-DAO')

from typing import Union, List
from process import Process
from mongoDAO import MongoOutputDAO
import nltk
import re
import collections

class WordFrequency(Process):
    def process_raw_tweets(self, tweet_doc, output_collection_name, config):
        tweet_ID = tweet_doc['tweetID']
        text = tweet_doc['text']

        # process 
        processed_text_list = self._process_tweet_text(text)

        # store in output_collection_name
        processed_tweet_doc = {
            'tweetID': tweet_ID, 
            'processed-text-list': processed_text_list
        }
        if output_collection_name not in self.output_DAOs:
            # dynamically create new DAO
            self.output_DAOs[output_collection_name] = self.DAO_factory.create_DAO_from_config("output", config) 
        self.output_DAOs[output_collection_name].create(processed_tweet_doc)

    def generate_global_word_frequency_vector(self, date, output_collection_name, date_input_config="", output_config=""):
        # TODO: date is currently just a string rep; maybe wanna make it datetime; or leave as is, since easier
        # to access data base given the string form of the date

        # get the collection that has the processed tweets from date
        if date not in self.output_DAOs:
            # dynamically create new DAO
            self.input_DAOs[date] = self.DAO_factory.create_DAO_from_config("input", date_input_config)
        daily_processed_tweets = self.input_DAOs[date]

        words = []
        for processed_tweet in daily_processed_tweets:
            words.extend(processed_tweet['processed-text-list'])

        word_freq_vector = self._get_word_frequency_vector(words)
        word_freq_vector_doc = {
            "Date": date,
            "WordFreqVector": word_freq_vector
        }

        if output_collection_name not in self.output_DAOs:
            # dynamically create new DAO
            self.output_DAOs[output_collection_name] = self.DAO_factory.create_DAO_from_config("output", output_config) 
        self.output_DAOs[output_collection_name].create(word_freq_vector_doc)

    def generate_user_word_frequency_vector(self, date, user, output_collection_name, date_input_config="", output_config=""):
        # get user timeline tweets from database
        if date not in self.output_DAOs:
            # dynamically create new DAO
            self.input_DAOs[date] = self.DAO_factory.create_DAO_from_config("input", date_input_config)
        user_daily_tweets = self.input_DAOs[date]

        # process 
        words = []
        for tweet in user_daily_tweets:
            text = user_daily_tweets['text']
            processed_text_list = self._process_tweet_text(text)
            words.extend(processed_text_list)
        
        word_freq_vector = self._get_word_frequency_vector(words)
        
        # TODO: rethink structure
        word_freq_vector_doc = {
            "User": user,
            "Date": date,
            "WordFreqVector": word_freq_vector
        }


        if output_collection_name not in self.output_DAOs:
            # dynamically create new DAO
            self.output_DAOs[output_collection_name] = self.DAO_factory.create_DAO_from_config("output", output_config) 
        self.output_DAOs[output_collection_name].create(word_freq_vector_doc)

    def _get_word_frequency_vector(self, words):
        word_freq_vector = collections.Counter()
        
        for word in words:
            word_freq_vector[word] += 1

        return word_freq_vector

    def _process_tweet_text(self, text):
        text = text.lower()
        
        # filter links, numbers, and emojis
        text = re.sub(r"\bhttps:\S*\b", "", text)
        text = re.sub(r"\b\d*\b", "", text)
        text = re.sub(r"[^\w\s@#]", "", text)

        processed_text_list = text.split()
        # hashtags, usernames
        for i in range(0, len(processed_text_list)):
            word = processed_text_list[i]
            if '#' in word or '@' in word:
                processed_text_list[i] = ''

        processed_text_list = list(filter(lambda x: x != '', processed_text_list))
        
        # remove stop words
        nltk.download('stopwords') # TODO: maybe not efficient to do this here`
        stopwords = set(nltk.corpus.stopwords.words('english'))
        stopwords.add('amp')
        for word in stopwords:
            if word in processed_text_list:
                #TODO extract
                processed_text_list.remove(word)

        # run stemming
        sno = nltk.stem.SnowballStemmer('english')
        processed_text_list = [sno.stem(word) for word in processed_text_list]

        return processed_text_list

    def generate_relative_user_word_frequency_vector():
        # get user_word_frequency vector

        # get global word frequency vector 

        # for each word in user vector
            # if in global
                # get relative
            # else 
                # get 


# TODO: 
# maybe we can have a general word frequency helper
# make processing helpers
