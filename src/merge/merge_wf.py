from pymongo import MongoClient
from show_wordcount import wordcount


def merge(dict1, dict2, wordcount1, wordcount2):
    total_wordcount = wordcount1 + wordcount2
    for item in dict2.keys():
        if item in dict1:
            dict1[item] = (dict1[item]*wordcount1 + dict2[item]*wordcount2) / total_wordcount
        else:
            dict1[item] = dict2[item] * wordcount1 / total_wordcount
    return dict1



if __name__ == "__main__":
    # input database
    new_db_name = "WordFrequency-Test"
    orig_db_name = "WordFrequency"

    #input dada collection
    collection_name = "GlobalWordFrequency"

    #location in MongoDB
    client = MongoClient('mongodb://localhost:27017')

    #Combine WordFrequency
    new_db = client[new_db_name]
    orig_db = client[orig_db_name]

    new_collection = new_db[collection_name]
    orig_collection = orig_db[collection_name]

    new_wf = new_collection.find_one({}, {'_id': 0})
    orig_wf = orig_collection.find_one({}, {'_id': 0})

    #wordcount
    new_wordcount = wordcount(new_db_name)
    orig_wordcount = wordcount(orig_db_name)

    #merge
    merge_wf = merge(new_wf, orig_wf, new_wordcount, orig_wordcount)

    #insert
    new_collection.replace_one({},merge_wf)
