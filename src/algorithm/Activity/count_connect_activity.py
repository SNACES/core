from typing import Dict
from src.algorithm.DAO.CountConnectDAOFactory import CountConnectDAOFactory
from src.algorithm.process.CountConnect import CountConnect

class CountConnectActivity():
    """
    Get rid of inactive users.
    """
    def __init__(self, config: Dict):
        self.count_connect = None

        self.configure(config)
    
    def configure(self, config: Dict):
        if config is not None:
            input_datastore = config["input-datastore"]
            input_cluster = input_datastore["Cluster"]
            input_friends = input_datastore["User-Friends"]

            cluster_getter = CountConnectDAOFactory.create_cluster_getter(input_cluster)
            friends_getter = CountConnectDAOFactory.create_friends_getter(input_friends)

            count_connect = CountConnect(cluster_getter, friends_getter)

            self.count_connect= count_connect
    
    def count_connect_between_cluster(self, cluster_num_1, cluster_num_2, base_user, cluster_type):
        self.count_connect.count_connect_between_cluster(cluster_num_1, cluster_num_2, base_user, cluster_type)