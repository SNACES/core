class MongoDAO():
    def __init__(self):
        self.collection = None

    def set_collection(self, collection):
        self.collection = collection
