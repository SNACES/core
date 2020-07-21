from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
test_db = client['test']
nested_col = test_db['nestedCol']

nested_col.insert_one({
    'nest': [{'is_nice': True, 'x': 5}, {'is_cool': True, 'x': 5}]
})

doc_list = nested_col.find({
    'nest.is_nice': True
})

for doc in doc_list:
    print(doc['nest'])

