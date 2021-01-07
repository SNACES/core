class MongoTopUsersSetter():
    def __init__(self):
        self.collection = None

    def set_collection(self, collection) -> None:
        self.collection = collection

    def set_top_users(self, cluster_num, base_user, cluster_type, top_users):
        self.collection.insert_one({"base_user": base_user, 
                                    "cluster_type": cluster_type, 
                                    "cluster_num": cluster_num, 
                                    "top_users": top_users})