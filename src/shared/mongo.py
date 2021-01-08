from pymongo import MongoClient
import datetime


def get_collection_from_config(mongo_config, gen_new_collection=False):
    db_location = mongo_config['location']

    if gen_new_collection:
        db_name = mongo_config['datastore-name' + str(datetime.date.today())]
    else:
        db_name = mongo_config['datastore-name']

    client = MongoClient(db_location)
    db = client[db_name]
    collection_name = mongo_config['collection-name']

    return db[collection_name]
