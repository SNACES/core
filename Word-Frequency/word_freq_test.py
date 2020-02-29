import os
import sys
sys.path.append('../Twitter-Download')

from word_frequency import WordFrequency, daterange
from twitterDownloader import TwitterTweetDownloader, TwitterFriendsDownloader
import datetime

port = "2223"

start_date = datetime.datetime(2019, 2, 1, 0, 0, 0)
end_date = datetime.datetime(2020, 2, 1, 0, 0, 0)
id = "david_madras"
word_frequency = WordFrequency(os.getcwd() + "/../General/ds-init-config.yaml")

# get global word frequency vector
input_config = {
    "project-name": "Word Frequency",
    "datastore-name": "ProcessedTweetDS",
    # "collection-name": "",
    "type": "MongoDB",
    "location": "mongodb://localhost:" + port
}
output_config = {
    "project-name": "WordFrequency",
    "datastore-name": "WordFrequencyVector-Test",
    "type": "MongoDB",
    "location": "mongodb://localhost:" + port
}

# for date in daterange(start_date, end_date):
#     word_frequency.generate_global_word_frequency_vector(date, "GlobalWordFrequency", input_config, output_config)


def download_user_relative_word_freq(start_date, end_date, id):
    # download tweets for a user
    downloader = TwitterTweetDownloader(os.getcwd() + "/../General/ds-init-config.yaml")
    downloader.get_tweets_by_timeframe_user(start_date, end_date, 10, id, None)

    # get user word frequency vector for timeframe
    input_config = {
        "project-name": "General",
        "datastore-name": "TwitterTweetDownload",
        "collection-name": "getTweetsByTimeframeUser",
        "type": "MongoDB",
        "location": "mongodb://localhost:" + port
    }
    output_config = {
        "project-name": "Word Frequency",
        "datastore-name": "WordFrequencyVector-Test",
        "type": "MongoDB",
        "location": "mongodb://localhost:" + port
    }
    for date in daterange(start_date, end_date):
        word_frequency.generate_user_word_frequency_vector(date, id, "UserWordFrequency", input_config, output_config)

    # get relative word frequency for david_madras
    global_word_freq_config = {
        "project-name": "Word Frequency",
        "datastore-name": "WordFrequencyVector-Test",
        "collection-name": "GlobalWordFrequency",
        "type": "MongoDB",
        "location": "mongodb://localhost:" + port
    }
    user_word_freq_config = {
        "project-name": "Word Frequency",
        "datastore-name": "WordFrequencyVector-Test",
        "collection-name": "UserWordFrequency",
        "type": "MongoDB",
        "location": "mongodb://localhost:" + port
    }
    output_config = {
        "project-name": "WordFrequency",
        "datastore-name": "WordFrequencyVector-Test",
        "type": "MongoDB",
        "location": "mongodb://localhost:" + port
    }
    # word_frequency.generate_relative_user_word_frequency_vector(start_date, end_date, id, user_word_freq_config, global_word_freq_config, "RelativeUserWordFrequency", output_config)

friend_downloader = TwitterFriendsDownloader(os.getcwd() + "/../General/ds-init-config.yaml")
users_following = friend_downloader.get_friends_by_screen_name(id, 100)
# print(users_following)
for user in users_following:
    download_user_relative_word_freq(start_date, end_date, user)