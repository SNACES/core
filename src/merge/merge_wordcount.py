from pymongo import MongoClient


def merge(dict1, dict2):
    for item in dict2.keys():
        if item in dict1:
            dict1[item] += dict2[item]
        else:
            dict1[item] = dict2[item]
    return dict1


if __name__ == "__main__":
    # input database
    new_db_name = "WordFrequency-Test"
    orig_db_name = "WordFrequency"

    #input dada collection
    collection_name = "GlobalWordCount"

    #location in MongoDB
    client = MongoClient('mongodb://localhost:27017')

    #Combine WordFrequency
    new_db = client[new_db_name]
    orig_db = client[orig_db_name]

    new_collection = new_db[collection_name]
    orig_collection = orig_db[collection_name]

    new_wf = new_collection.find_one()
    orig_wf = orig_collection.find_one()

    #merge
    merge_wf = merge(new_wf, orig_wf)

    #insert
    new_collection.insert_one(merge_wf)
