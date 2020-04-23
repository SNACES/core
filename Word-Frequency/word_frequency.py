import sys
sys.path.append('../General')
sys.path.append('../General/Concrete-DAO')

from typing import Union, List
from process import Process
from mongoDAO import MongoOutputDAO
import nltk
import re
import collections
import datetime
from word_freq_mongo_output_dao import WordFrequencyMongoOutputDAO
from word_freq_mongo_input_dao import WordFrequencyMongoInputDAO

class WordFrequency(Process):
    def process_raw_tweets(self, tweet_ID, text, output_collection_name):
        # process 
        processed_text_list = self._process_tweet_text(text)

        # store in output_collection_name
        self.output_DAOs[output_collection_name].store_processed_tweet(tweet_ID, processed_text_list)

    def generate_global_word_frequency_vector(self, date: datetime, input_collection_name, output_collection_name):
        # TODO: finish fixing this
        
        daily_processed_tweet_text = self.input_DAOs[input_collection_name].get_processed_tweet
        
        words = []
        for processed_tweet in daily_processed_tweet_text:
            words.extend(processed_tweet['processed-text-list'])
        
        word_freq_vector = self._get_word_frequency_vector(words)
        if word_freq_vector:
            self.output_DAOs[output_collection_name].store_daily_global_word_frequency_vector

    def generate_user_word_frequency_vector(self, date: datetime, user, output_collection_name, date_input_config=None, output_config=None):
        # TODO: handle default value for date_input_config
        input_name = date_input_config['collection-name']
        if input_name not in self.input_DAOs:
            # dynamically create new DAO
            self.input_DAOs[input_name] = self.DAO_factory.create_DAO_from_config("input", date_input_config)
        # TODO: dates issue
        collection = self.input_DAOs[input_name].read({ "id": user, "start_date": date })
        user_daily_tweet_text = [tweet['text'] for tweets_doc in collection for tweet in tweets_doc['tweets']]

        # process 
        words = []
        for text in user_daily_tweet_text:
            processed_text_list = self._process_tweet_text(text)
            words.extend(processed_text_list)
        # print(words)
        
        word_freq_vector = self._get_word_frequency_vector(words)
        # print(word_freq_vector)
        if word_freq_vector:
            word_freq_vector_doc = {
                "User": user,
                "Date": date,
                "WordFreqVector": word_freq_vector
            }

            # output_collection_name generated based on the date
            # output_collection_name = "UserWordFrequency"
            output_config['collection-name'] = output_collection_name
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
        
        # run stemming: it's important to run this first before stop words for cases such as that's
        sno = nltk.stem.SnowballStemmer('english')
        processed_text_list = [sno.stem(word) for word in processed_text_list]

        # remove stop words
        # nltk.download('stopwords') # TODO: maybe not efficient to do this here`
        stopwords = set(nltk.corpus.stopwords.words('english'))
        stopwords.add('amp')
        for word in stopwords:
            if word in processed_text_list:
                #TODO extract
                while (processed_text_list.count(word)): 
                    processed_text_list.remove(word)

        return processed_text_list

    def generate_relative_user_word_frequency_vector(self, start_date: datetime, 
                end_date: datetime, user, user_word_freq_config={}, global_word_freq_config=None, output_collection_name="", output_config=None):
        # get user_word_frequency vectors for timeframe
            # combine the counters to get megacounter
        input_name = global_word_freq_config['collection-name']
        if input_name not in self.input_DAOs:
            # dynamically create new DAO
            self.input_DAOs[input_name] = self.DAO_factory.create_DAO_from_config("input", global_word_freq_config)

        daily_global_vectors = []
        for date in daterange(start_date, end_date): # TODO: modulaize this for global and user
            # print(date)
            # date = date.strftime("%Y-%m-%d")
            query = self.input_DAOs[input_name].read({"Date": date})
            daily_vectors = [collections.Counter(daily_vector_doc["WordFreqVector"]) for daily_vector_doc in query]
            daily_global_vectors.extend(daily_vectors)
        # print(daily_global_vectors)
        timeframe_global_word_freq = sum(daily_global_vectors, collections.Counter())
        
        # get global word frequency vectors for time frame
            # combine the counters to get megacounter
        input_name = user_word_freq_config['collection-name']
        if input_name not in self.input_DAOs:
            # dynamically create new DAO
            self.input_DAOs[input_name] = self.DAO_factory.create_DAO_from_config("input", user_word_freq_config)

        daily_user_vectors = []
        for date in daterange(start_date, end_date):
            query = self.input_DAOs[input_name].read({"User": user, "Date": date})
            daily_vectors = [collections.Counter(daily_vector_doc["WordFreqVector"]) for daily_vector_doc in query]
            daily_user_vectors.extend(daily_vectors)
        timeframe_user_word_freq = sum(daily_user_vectors, collections.Counter())
        # print(timeframe_user_word_freq)
        # print(timeframe_global_word_freq)
        # for each word in user vector
            # if in global
                # get relative
            # else 
                # get 
        user_words_not_in_global = []
        relative_word_freq = {}
        for word in timeframe_user_word_freq:
            user_word_count = timeframe_user_word_freq[word]
            if user_word_count >= 3:
                if word in timeframe_global_word_freq:
                    global_word_count = timeframe_global_word_freq[word]
                    relative_word_freq[word] = user_word_count / global_word_count
                else:
                    user_words_not_in_global.append(word)

        # store  
        output_doc = {
            "User": user,
            "StartDate": start_date,
            "EndDate": end_date,
            "RelativeWordFrequency": relative_word_freq,
            "UserWordsNotInGlobal": user_words_not_in_global
        }
        # print(output_doc)
        output_config["collection-name"] = output_collection_name
        if output_collection_name not in self.output_DAOs:
            # dynamically create new DAO
            self.output_DAOs[output_collection_name] = self.DAO_factory.create_DAO_from_config("output", output_config) 
        self.output_DAOs[output_collection_name].create(output_doc)
        

# TODO: maybe make this a general helper
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)      


# TODO: 
# maybe we can have a general word frequency helper
# make processing helpers
