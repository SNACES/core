import networkx as nx

class SocialGraphMongoSetDAO:
    def __init__(self):
        self.user_friends_graph_collection = None

    def store_user_friends_graph(self, user, graph):
        adj_list = [item for item in nx.generate_adjlist(graph)]
        self.user_friends_graph_collection.insert_one({
            'user': user, 
            'adj_list': adj_list
        })

