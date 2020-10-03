from pymongo import MongoClient
from collections import Counter

def wordcount(wf_db_name:str):
    """
    Return the total number of words under the database wf_db_name.

    @param wf_db_name: name of the database
    @return: number of words in the GlobalWordCount collection
    """
    #client
    client = MongoClient('mongodb://localhost:27017/')

    #database
    wf_db = client[wf_db_name]

    #collection
    global_collection_name = "GlobalWordCount"
    wc_new_col = wf_db[global_collection_name]

    #how many words
    return(len(wc_new_col.find_one()))


if __name__ == "__main__":
    print(wordcount("WordFrequency"))
    print(wordcount("WordFrequency-Test"))