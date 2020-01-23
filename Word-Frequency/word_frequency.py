import sys
sys.path.append('../General')
sys.path.append('../General/Concrete-DAO')

from typing import Union, List
from process import Process
from mongoDAO import MongoOutputDAO
import nltk
import re

class WordFrequency(Process):
    def process_raw_tweets(self, tweet_doc, output_collection_name, config):
        tweet_ID = tweet_doc['tweetID']
        text = tweet_doc['text']

        # process 
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
        #  text = text.lower()
        sno = nltk.stem.SnowballStemmer('english')
        processed_text_list = [sno.stem(word) for word in processed_text_list]

        processed_tweet_doc = {'tweetID': tweet_ID, 'processed-text-list': processed_text_list}

        if output_collection_name not in self.output_DAOs:
            # dynamically create new DAO
            self.output_DAOs[output_collection_name] = self.DAO_factory.create_DAO_from_config("output", config) 
        self.output_DAOs[output_collection_name].create(processed_tweet_doc)

    # def generate_global_word_frequency_vector(self, date, output_collection_name, config):
        

    #     if output_collection_name not in self.output_DAOs:
    #         # dynamically create new DAO
    #         self.output_DAOs[output_collection_name] = self.DAO_factory.create_DAO_from_config("output", config) 
    #     self.output_DAOs[output_collection_name].create(processed_tweet_doc)