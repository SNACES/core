import os
import sys
sys.path.append('../Twitter-Download')
from twitterDownloader import TwitterTweetDownloader, TwitterFriendsDownloader

import pymongo
import datetime
from word_frequency import WordFrequency, daterange
from pymongo import MongoClient
from collections import Counter

ds_location = 'mongodb://localhost:27017' 
word_frequency = WordFrequency(os.getcwd() + "/../General/ds-init-config.yaml")
client = MongoClient(ds_location)
# get global word freq vector from Thomas's database
db = client['globalData']
collection = db['wordCount']
result = collection.find()
global_word_freq_vector = Counter()
for doc in result:
    for word in doc:
        if word != '_id':
            global_word_freq_vector[word] = doc[word]

# get list of david madras followers from Thomas's code
friend_downloader = TwitterFriendsDownloader(os.getcwd() + "/../General/ds-init-config.yaml")
madras_following_users = friend_downloader.get_friends_by_screen_name("david_madras", 400)

# based on Thomas's user database, calculate the user word frequencies and store in my format
db = client['productionFunction']
collection = db['users']

users_in_db = []
for user_handle in madras_following_users:
    result = collection.find({'handle': user_handle})
    for doc in result:
        if doc['start'] == datetime.datetime(2018, 9, 1, 0, 0, 0) and\
         doc['end'] == datetime.datetime(2019, 9, 1, 0, 0, 0) and user_handle == doc['handle']:
            words = []
            # for tweet_text in doc['tweets']:
            #     processed_text_list = word_frequency._process_tweet_text(tweet_text)
            #     words.extend(processed_text_list)

            for tweet_text in doc['retweets']:
                processed_text_list = word_frequency._process_tweet_text(tweet_text[0])
                words.extend(processed_text_list)
                
            # get word frequency
            user_word_freq_vector = word_frequency._get_word_frequency_vector(words)

            # store in db
            word_freq_db = client['WordFreq-Retweets']
            user_word_freq_collection = word_freq_db['UserWordFreq']
            user_word_freq_collection.insert_one({
                'User': user_handle,
                'UserWordFreqVector': user_word_freq_vector  
            })

            users_in_db.append(user_handle)

# calculate user relative word freq
word_freq_db = client['WordFreq-Retweets']
user_word_freq_collection = word_freq_db['UserWordFreq']
result = user_word_freq_collection.find()
for doc in result:
    user_handle = doc['User']
    # get user word freq
    user_word_freq_vector = doc['UserWordFreqVector']
    user_words_not_in_global = []
    relative_word_freq = {}
    for word in user_word_freq_vector:
        user_word_count = user_word_freq_vector[word]
        if user_word_count >= 3:
            if word in global_word_freq_vector:
                global_word_count = global_word_freq_vector[word]
                relative_word_freq[word] = user_word_count / global_word_count
            else:
                user_words_not_in_global.append(word)

    user_word_freq_collection = word_freq_db['UserRelativeWordFreq']
    user_word_freq_collection.insert_one({
        "User": user_handle,
        "RelativeWordFrequency": relative_word_freq,
        "UserWordsNotInGlobal": user_words_not_in_global
    })

# store the list of users from which we've gotten our relative user freq
db = client['WordFreq-Retweets']
collection = db['Users']
collection.insert_one({
    'Users': users_in_db,
    'InitialUsersSet': madras_following_users
})
      
# word_frequency = WordFrequency(os.getcwd() + "/../General/ds-init-config.yaml")
# print(word_frequency._process_tweet_text("thatve thatss yeas"))
