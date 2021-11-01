import networkx as nx

class SocialGraphMongoSetDAO:
    def __init__(self):
        self.user_friends_graph_collection = None

    def store_user_friends_graph(self, user, graph):
        adj_list = [item for item in nx.generate_adjlist(graph)]
        
        # Note: we only want to store one social graph per user
        user_doc = self.user_friends_graph_collection.find_one({
            'user': user
        })
        
        if user_doc:
            # Update adj list
            user_doc['adj_list'] = adj_list
            self.user_friends_graph_collection.replace_one({
                'user': user
            }, user_doc)
        else:
            self.user_friends_graph_collection.insert_one({
                'user': user, 
                'adj_list': adj_list
            })

