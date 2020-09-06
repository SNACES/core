from pymongo import MongoClient

def get_collection_from_config(mongo_config):
    db_location = mongo_config['location'] 
    db_name = mongo_config['datastore-name']
    
    client = MongoClient(db_location)
    db = client[db_name]
    collection_name = mongo_config['collection-name']

    return db[collection_name]