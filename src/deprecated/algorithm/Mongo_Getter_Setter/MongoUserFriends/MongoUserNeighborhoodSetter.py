class MongoLocalNeighborhoodSetter():
    def __init__(self):
        self.collection = None

    def set_collection(self, collection) -> None:
        self.collection = collection

    def store_user_neighbourhood(self, local_neighbourhood):
        self.collection.insert_one({"local_neighborhood":local_neighbourhood})
