import networkx as nx

class SocialGraphMongoGetDAO:
    def __init__(self):
        self.user_friends_graph_collection = None

    def get_user_to_friends_graph(self, user):
        query = self.user_friends_graph_collection.find_one({'user': user})
        graph = nx.parse_adjlist(query['adj_list'])
        
        return graph


