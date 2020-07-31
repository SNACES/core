import nltk
import re
import datetime

class RawTweetProcessor():
    def __init__(self):
        nltk.download('stopwords')

    def gen_processed_global_tweets(self, input_dao, output_dao):
        """
        Assume that the input dao contains a random stream of tweets. 
        The common format is: [tweet text].
        Return and store processed global tweets.
        Update global tweet database to reflect processed tweet state.
        """
        
        global_tweet_list = input_dao.get_global_tweets()
        processed_global_tweet_list = list(map(self._process_tweet_text, global_tweet_list))
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

        user_to_tweets = input_dao.get_user_tweets()
        user_to_processed_tweet_list = {}

        for user in user_to_tweets:
            tweet_list = user_to_tweets[user]
            processed_tweet_list = map(self._process_tweet_text, tweet_list)
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
        stopwords = set(nltk.corpus.stopwords.words('english'))
        stopwords.add('amp')
        for word in stopwords:
            if word in processed_text_list:
                # TODO: extract
                while (processed_text_list.count(word)): 
                    processed_text_list.remove(word)

        return processed_text_list