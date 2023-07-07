from src.model.cluster import Cluster
import src.dependencies.injector as sdi
from src.shared.utils import get_project_root
from src.clustering_experiments import ranking_users_in_clusters as rank
import pygraphviz as pgv
DEFAULT_PATH = str(get_project_root()) + "/src/scripts/config/create_social_graph_and_cluster_config.yaml"

class ClusterNode:
    """A node in a tree structure, which holds info about a cluster

    === Attributes ===
    root: the cluster represented by the node
    thresh: the threshold used to generate root
    children: list of child nodes of this node
    parent: the parent of this node
    """

    def __init__(self, thresh: float, root: Cluster, top_users=None, children=None, parent=None):
        self.root = root
        self.parent = parent
        self.threshold = thresh
        self.top_users = top_users
        self.id = None

        if children is None:
            children = []
        self.children = children

    def display(self, indent=0):
        """Display the tree rooted at current node"""
        print(("   " * indent) + str(self.threshold))
        for child in self.children:
            child.display(indent + 1)

    def display_cluster(self, G, id, file_path, indent=0):
        """Display the tree rooted at current node"""
        self.id = id
        self.root.id = id
        path = DEFAULT_PATH
        cluster = self.root
        injector = sdi.Injector.get_injector_from_file(path)
        dao_module = injector.get_dao_module()
        user_getter = dao_module.get_user_getter()
        base_user = user_getter.get_user_by_id(cluster.base_user)
        users = []
        for user in cluster.users:
            users.append(user_getter.get_user_by_id(user).screen_name)
        users.sort()
        top_10 = self.top_users
        if self.parent is None:
            l = 0
            t = 0
        else:
            l = len(self.parent.root.users)
            t = self.parent.threshold

        rounded_t = round(self.threshold, 4)
        text = f"{('   ' * indent)} id={id}, {str(rounded_t)}, {len(users)}, {top_10}, {l}, {round(t, 4)}"
        #print(text)
        with open(file_path, "a") as f:
            f.write(str(text) + "\n")
            f.close()

        # Draw the graph
        G.add_node(f"t={rounded_t}\n size={len(users)}\n id={id}")
        if self.parent is not None:
            G.add_edge(f"t={round(t, 4)}\n size={l}\n id={id[:-1]}", f"t={rounded_t}\n size={len(users)}\n id={id}")
        for i, child in enumerate(self.children):
            child.display_cluster(G, id + str(i), file_path, indent + 1)

        












