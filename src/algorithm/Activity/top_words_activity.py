from typing import Dict
from src.algorithm.DAO.TopWordsDAOFactory import TopWordsDAOFactory
from src.algorithm.process.top_words import TopWords

class TopWordsActivity():
    """
    Get rid of inactive users.
    """
    def __init__(self, config: Dict):
        self.top_words = None

        self.configure(config)
    
    def configure(self, config: Dict):
        if config is not None:
            input_datastore = config["input-datastore"]
            input_cluster = input_datastore["Cluster"]
            input_wordfrequency = input_datastore["WordFrequency"]

            cluster_getter = TopWordsDAOFactory.create_cluster_getter(input_cluster)
            wordfrequency_getter = TopWordsDAOFactory.create_wordfrequency_getter(input_wordfrequency)

            output_datastore = config["output-datastore"]
            output_top_words = output_datastore["TopWords"]

            top_words_setter = TopWordsDAOFactory.create_setter(output_top_words)

            top_words = TopWords(cluster_getter, wordfrequency_getter, top_words_setter)

            self.top_words = top_words
    
    def find_top_words(self, cluster_num, base_user, cluster_type):
        self.top_words.find_top_words(cluster_num, base_user, cluster_type)
    

