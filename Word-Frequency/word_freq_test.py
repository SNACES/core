import os
import sys
sys.path.append('../Twitter-Download')

from word_frequency import WordFrequency
from twitterDownloader import TwitterTweetDownloader
import datetime

port = "27017"

start_date = datetime.datetime(2019, 12, 1, 0, 0, 0)
end_date = datetime.datetime(2020, 2, 4, 0, 0, 0)
id = "david_madras"

# download tweets for a user
downloader = TwitterTweetDownloader(os.getcwd() + "/../General/ds-init-config.yaml")
# downloader.get_tweets_by_timeframe_user(start_date, end_date, 10, id, None)

# get user word frequency vector
word_frequency = WordFrequency(os.getcwd() + "/../General/ds-init-config.yaml")
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
# word_frequency.generate_user_word_frequency_vector(start_date, id, "UserWordFrequency", input_config, output_config)

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
# date = datetime.datetime(2020, 2, 3, 0, 0, 0)
# word_frequency.generate_global_word_frequency_vector(start_date, "GlobalWordFrequency", input_config, output_config)

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
word_frequency.generate_relative_user_word_frequency_vector(start_date, end_date, id, user_word_freq_config, global_word_freq_config, output_config)