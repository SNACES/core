from typing import Dict
from src.algorithm.DAO.CountOverlapDAOFactory import CountOverlapDAOFactory
from src.algorithm.process.CountOverlap import CountOverlap

class CountOverlapActivity():
    """
    Get rid of inactive users.
    """
    def __init__(self, config: Dict):
        self.count_overlap = None

        self.configure(config)
    
    def configure(self, config: Dict):
        if config is not None:
            input_datastore = config["input-datastore"]
            input_cluster_1 = input_datastore["Cluster1"]
            input_cluster_2 = input_datastore["Cluster2"]

            cluster_1_getter = CountOverlapDAOFactory.create_cluster_getter(input_cluster_1)
            cluster_2_getter = CountOverlapDAOFactory.create_cluster_getter(input_cluster_2)

            count_overlap = CountOverlap(cluster_1_getter, cluster_2_getter)

            self.count_overlap= count_overlap
    
    def count_overlap_between_cluster(self, cluster_num_1, cluster_num_2, base_user, cluster_type_1, cluster_type_2):
        self.count_overlap.count_connect_between_cluster(cluster_num_1, cluster_num_2, base_user, cluster_type_1, cluster_type_2)