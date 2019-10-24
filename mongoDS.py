from datastore import DataStore
from pymongo import MongoClient

class MongoDS(DataStore):
    def __init__(self, ds_location, mongo_database_name):
        self.client = MongoClient(ds_location) # 'mongodb://localhost:27017/'
        self.db = self.client[mongo_database_name] # 'temp-twitter'

    def create(self, name, items):
        collection = self.db[name]
        collection.insert_one(items) 

    def read(self, name, query):
        collection = self.db[name]
        collection.find(query)

    def update(self, name, items):
        pass
    
    def delete(self, name):
        pass