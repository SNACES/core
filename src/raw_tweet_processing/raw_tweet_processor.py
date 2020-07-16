import nltk
import re
import datetime
from functools import reduce

from src.general.process import Process

class RawTweetProcessor(Process):
    def gen_processed_global_tweets(self, input_dao, output_dao):
        """
        Assume that the input dao contains a random stream of tweets. 
        The common format is: [tweet text].
        Return and store processed global tweets.
        Update global tweet database to reflect processed tweet state.
        """
        
        global_tweet_list = input_dao.get_global_tweets()
        processed_global_tweet_list = list(reduce(_process_tweet_text, global_tweet_list))
        output_dao.store_global_processed_tweets(processed_global_tweet_list)
        output_dao.update_global_tweet_state()

        return processed_global_tweet_list

    def gen_processed_user_tweets(self, input_dao, output_dao):
        """
        Assume that the input dao contains tweets associated with users. 
        The common format is: {user: [tweet text]}.
        Return and store processed user tweets.
        Update user tweet database to reflect processed tweet state.
        """

        user_tweet_list = input_dao.get_user_tweets()
        user_to_processed_tweet_list = {}

        for user in user_to_processed_tweet_list:
            tweet_list = user_to_processed_tweet_list[user]
            processed_tweet_list = reduce(_process_tweet_text, tweet_list)

            user_to_processed_tweet_list[user] = processed_tweet_list

        output_dao.store_user_processed_tweets(user_to_processed_tweet_list)
        output_dao.update_user_tweet_state()

        return user_to_processed_tweet_list

    def _process_tweet_text(self, text):
        text = text.lower()
        
        # Filter links, numbers, and emojis
        text = re.sub(r"\bhttps:\S*\b", "", text)
        text = re.sub(r"\b\d*\b", "", text)
        text = re.sub(r"[^\w\s@#]", "", text)

        processed_text_list = text.split()
        # Hashtags, usernames
        for i in range(0, len(processed_text_list)):
            word = processed_text_list[i]
            if '#' in word or '@' in word:
                processed_text_list[i] = ''

        processed_text_list = list(filter(lambda x: x != '', processed_text_list))
        
        # Run stemming: it's important to run this first before stop words for cases such as that's
        sno = nltk.stem.SnowballStemmer('english')
        processed_text_list = [sno.stem(word) for word in processed_text_list]

        # Remove stop words
        nltk.download('stopwords') # TODO: maybe not efficient to do this here`
        stopwords = set(nltk.corpus.stopwords.words('english'))
        stopwords.add('amp')
        for word in stopwords:
            if word in processed_text_list:
                # TODO: extract
                while (processed_text_list.count(word)): 
                    processed_text_list.remove(word)

        return processed_text_list
    
    # def get_processed_tweet(self, tweet_ID, processed_text_list):
    #     # Old Format.
    #     formatted_date = date.strftime("%Y-%m-%d")
        
    #     # get the collection that has the processed tweets from date
    #     input_name = "({})-ProcessedTweets".format(formatted_date) 
    #     collection = self.input_DAOs[input_name]
    #     daily_processed_tweets = self.input_DAOs[input_name].read()
    #     daily_processed_tweet_text = [processed_tweet for processed_tweet in daily_processed_tweets]

    #     return daily_processed_tweet_text

    # def process_raw_tweets(self, tweet_ID, text, output_collection_name):
    #     # process 
    #     processed_text_list = self._process_tweet_text(text)

    #     # store in output_collection_name
    #     self.output_DAOs[output_collection_name].store_processed_tweet(tweet_ID, processed_text_list)
        