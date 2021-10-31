from src.dao.global_word_frequency.global_word_frequency_dao_factory import GlobalWordFrequencyDAOFactory
from src.dao.user_relative_word_frequency.user_relative_word_frequency_dao_factory import UserRelativeWordFrequencyDAOFactory
from src.dao.user_word_frequency.user_word_frequency_dao_factory import UserWordFrequencyDAOFactory
from src.dao.cluster_word_frequency.cluster_word_frequency_dao_factory import ClusterWordFrequencyDAOFactory
from src.dao.cluster_relative_word_frequency.cluster_relative_word_frequency_dao_factory import ClusterRelativeWordFrequencyDAOFactory
from src.process.word_frequency.cluster_word_frequency_processor import ClusterWordFrequencyProcessor
from typing import Dict


class ClusterWordFrequencyActivity():
    """
    """

    def __init__(self, config: Dict):
        self.cluster_word_frequency = None

        self.configure(config)

    def configure(self, config: Dict):
        if config is not None:
            # Configure input datastore
            input_datastore = config["input-datastore"]

            user_word_frequency = input_datastore["UserWordFrequency"]
            global_word_frequency = input_datastore["GlobalWordFrequency"]
            cluster_word_frequency = input_datastore["ClusterWordFrequency"]

            user_word_frequency_getter = UserWordFrequencyDAOFactory.create_getter(user_word_frequency)
            cluster_word_frequency_getter = ClusterWordFrequencyDAOFactory.create_getter(cluster_word_frequency)
            global_word_frequency_getter = GlobalWordFrequencyDAOFactory.create_getter(global_word_frequency)


            # Configure output datastore
            output_datastore = config["output-datastore"]

            cluster_word_frequency_out = output_datastore["ClusterWordFrequency"]
            relative_cluster_word_frequency_out = output_datastore["RelativeClusterWordFrequency"]

            cluster_word_frequency_setter = ClusterWordFrequencyDAOFactory.create_setter(cluster_word_frequency_out)
            relative_cluster_word_frequency_setter = ClusterRelativeWordFrequencyDAOFactory.create_setter(relative_cluster_word_frequency_out)

            self.cluster_word_frequency = ClusterWordFrequencyProcessor(user_word_frequency_getter, cluster_word_frequency_getter, 
                                                            cluster_word_frequency_setter, global_word_frequency_getter,
                                                            relative_cluster_word_frequency_setter)

    def get_cluster_word_frequency(self, seed_id):
        self.cluster_word_frequency.process_cluster_word_frequency_vector(seed_id)
        self.cluster_word_frequency.process_relative_cluster_word_frequency(seed_id)