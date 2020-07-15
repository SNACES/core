from datastore import *
from pymongo import MongoClient

class MongoDAO():
    def __init__(self, ds_location, mongo_database_name, collection_name):
        self.client = MongoClient(ds_location) # 'mongodb://localhost:27017/'
        self.db = self.client[mongo_database_name] # 'temp-twitter'
        self.collection = self.db[collection_name]
