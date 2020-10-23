import schedule
import daemon
import time

from src.shared.utils import get_project_root
from src.process.word_frequency.word_frequency import WordFrequency
from src.process.word_frequency.wf_config_parser import WordFrequencyConfigParser

def make_word_frequency():
    def global_word_count():
        word_frequency = WordFrequency()
        config_path = get_project_root() / 'src' / 'process' / 'word_frequency' / 'wf_config.yaml'
        word_frequency_parser = WordFrequencyConfigParser(config_path)
        processed_tweet_getter, _ = word_frequency_parser.create_getter_DAOs()
        processed_tweet_setter, wf_setter = word_frequency_parser.create_setter_DAOs()
        word_frequency.gen_global_word_count_vector(processed_tweet_getter, processed_tweet_setter, wf_setter)

    with daemon.DaemonContext(chroot_directory=None, working_directory='./'):
        # schedule every second, rather than every day
        schedule.every().day.at("0:00").do(global_word_count)

        while True:
            schedule.run_pending()
            time.sleep(1)
