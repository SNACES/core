import numpy

from pymongo import MongoClient
from collections import Counter

# TODO:
class MUISIMongoGetDAO():   
    def __init__(self):
        self.muisi_cluster_collection = None

    def get_clusters(self):
        clusters_list = self.muisi_cluster_collection.find()
        return clusters_list

# if __name__ == "__main__":
    # import doctest
    # doctest.testmod(extraglobs={'dao': MUISIInput()})
