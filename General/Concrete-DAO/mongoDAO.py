import sys
sys.path.append('../General')

from datastore import *
from pymongo import MongoClient

class MongoDAO():
    def __init__(self, ds_location, mongo_database_name, collection_name):
        self.client = MongoClient(ds_location) # 'mongodb://localhost:27017/'
        self.db = self.client[mongo_database_name] # 'temp-twitter'
        self.collection = self.db[collection_name]

"""
Concrete implementation of InputDAO that supports MongoDB.
"""
class MongoInputDAO(InputDAO, MongoDAO):
    def read(self, query=None):
        if query is None:
            return self.collection.find()
        else:
            return self.collection.find(query)

"""
Concrete implementation of OutputDAO that supports MongoDB.
"""
class MongoOutputDAO(OutputDAO, MongoDAO):
    def create(self, items):
        self.collection.insert_one(items) 