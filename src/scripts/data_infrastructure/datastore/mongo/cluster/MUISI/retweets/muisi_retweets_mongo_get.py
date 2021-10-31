import datetime
import numpy

from pymongo import MongoClient
from collections import Counter

# TODO:
class MUISIRetweetsMongoGetDAO():
    def __init__(self):
        self.muisi_retweets_cluster_collection = None
    
    def get_clusters(self):
        clusters_list = self.muisi_retweets_cluster_collection.find()
        return clusters_list

