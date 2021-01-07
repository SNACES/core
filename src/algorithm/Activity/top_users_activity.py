from typing import Dict
from src.algorithm.DAO.TopUsersDAOFactory import TopUsersDAOFactory
from src.algorithm.process.TopUsers import TopUsers

class TopUsersActivity():
    """
    Get rid of inactive users.
    """
    def __init__(self, config: Dict):
        self.top_users = None

        self.configure(config)
    
    def configure(self, config: Dict):
        if config is not None:
            input_datastore = config["input-datastore"]
            input_cluster = input_datastore["Cluster"]
            input_wordfrequency = input_datastore["RelativeWordFrequency"]
            input_topwords = input_datastore["TopWords"]

            cluster_getter = TopUsersDAOFactory.create_cluster_getter(input_cluster)
            wordfrequency_getter = TopUsersDAOFactory.create_wordfrequency_getter(input_wordfrequency)
            topwords_getter = TopUsersDAOFactory.create_topwords_getter(input_topwords)

            output_datastore = config["output-datastore"]
            output_top_users = output_datastore["TopUsers"]

            top_users_setter = TopUsersDAOFactory.create_topusers_setter(output_top_users)

            top_users = TopUsers(cluster_getter, wordfrequency_getter, topwords_getter, top_users_setter)

            self.top_users = top_users
    
    def find_top_users(self, cluster_num, base_user, cluster_type):
        self.top_users.find_top_users(cluster_num, base_user, cluster_type)

