class MongoTopWordsSetter():
    def __init__(self):
        self.collection = None

    def set_collection(self, collection) -> None:
        self.collection = collection

    def set_top_words(self, cluster_num, base_user, cluster_type, top_words):
        self.collection.insert_one({"base_user":base_user, 
                                    "cluster_type":cluster_type, 
                                    "cluster_num": cluster_num, 
                                    "top_words":top_words})