from src.model.cluster import Cluster

class ClusterNode:
    """A node in a tree structure, which holds info about a cluster

    === Attributes ===
    root: the cluster represented by the node
    thresh: the threshold used to generate root
    children: list of child nodes of this node
    parent: the parent of this node
    """

    def __init__(self, thresh: float, root: Cluster, children=None, parent=None):
        self.root = root
        self.parent = parent
        self.threshold = thresh

        if children is None:
            children = []
        self.children = children

    def display(self, indent=0):
        """Display the tree rooted at current node"""
        print(("   " * indent) + str(self.threshold))
        for child in self.children:
            child.display(indent + 1)











