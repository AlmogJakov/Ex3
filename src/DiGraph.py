from GraphInterface import GraphInterface


class DiGraph(GraphInterface):
    def __init__(self):
        self.graph = {}  # key = node key. value = node object
        self.ni = {}  # key = node key. value = (node neighbors dictionaries ->) key = neighbor-key. value = weight
        self.revers_ni = {}  # key = node key. value = tuple list of node neighbors keys (with reversed edges)
        self.edge_size = 0
        self.mc = 0

    """
    This method returns the number of vertices (nodes) in
    the graph. The implementation of the method is simply
    by returning 'graph' size.
    """
    def v_size(self) -> int:
        return len(self.graph)

    """
    This method returns the number of edges (directional graph).
    The implementation of the method is simply by returning
    edge_size variable.
    """
    def e_size(self) -> int:
        return self.edge_size

    """
    This method returns the Mode Count - for testing changes
    in the graph. The implementation of the method is simply
    by returning 'MC' variable.
    """
    def get_mc(self) -> int:
        return self.mc

    """
    This method returns a dict with all the nodes in the graph.
    the method is implemented by returning 'graph' dict.
    """
    def get_all_v(self) -> dict:
        return self.graph

    """
    This method returns a collection containing
    all the in edges connected to id1. the method returning null if
    node_id isn't in the graph. The implementation of the method is simply by
    returning the 'revers_ni' dict values (neighbors) of id1.
    """
    def all_in_edges_of_node(self, id1: int) -> dict:
        return self.revers_ni.get(id1)

    """
    This method returns a collection containing
    all the out edges connected to id1. the method returning null if
    node_id isn't in the graph. The implementation of the method is simply by
    returning the 'ni' dict values (neighbors) of id1.
    """
    def all_out_edges_of_node(self, id1: int) -> dict:
        return self.ni.get(id1)

    """
    This method connects an edge between id1 and id2, with a weight>=0.
    the method implemented only if id1 and id2 in the graph, id1!=id2 and w>=0. 
    if the edge already exists no action performed.
    if there is no such edge the method adds each Node to the list of neighbors
    [dict] of the other Node and updates 'edge_size' variable.
    if any action performed the method updates 'MC' variable.
    """
    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if not self.graph.__contains__(id1) or not self.graph.__contains__(id2) or weight < 0 or id1 == id2:
            return False
        if self.ni.get(id1).__contains__(id2):
            return False
        self.ni.get(id1).update({id2: weight})
        self.revers_ni.get(id2).update({id1: weight})
        self.edge_size = self.edge_size + 1
        self.mc = self.mc + 1
        return True

    """
    This method adds a new node to the graph with the given node key.
    if there is already a node with such a key no action performed.
    the method is implemented by adding the node to each dict in this class.
    if the method is implemented we update the MC (Mode Count).
    """
    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if self.graph.__contains__(node_id):
            return False
        new_node = NodeData()
        new_node.key = node_id
        new_node.pos = pos
        new_node.graph = self
        self.graph.update({node_id: new_node})
        self.ni.update({node_id: {}})
        self.revers_ni.update({node_id: {}})
        self.mc += 1
        return True

    """
    This method delete the node (with the given ID) from the graph
    and removes all edges which starts or ends at this node.
    the method return False if the Node isn't in the graph as requested.
    otherwise, the method performs an iteration on all the neighbors of the Node
    and removes all connected edges one by one while each step updates the MC (Mode Count). 
    afterwards the method removes the Node itself and update the MC (Mode Count) once again.
    finally the method returns True.
    """
    def remove_node(self, node_id: int) -> bool:
        if not self.graph.__contains__(node_id):
            return False
        for node in self.ni.get(node_id).keys():
            self.revers_ni.get(node).pop(node_id)
        ni_size = len(self.ni.get(node_id))
        self.ni.pop(node_id)
        self.edge_size = self.edge_size - ni_size
        self.mc = self.mc + ni_size
        self.edge_size = self.edge_size - len(self.revers_ni.get(node_id))
        for node in self.revers_ni.get(node_id):
            self.ni.get(node).pop(node_id)
            self.mc = self.mc + 1
        self.revers_ni.pop(node_id, None)
        self.graph.pop(node_id)
        self.mc = self.mc + 1
        return True

    """
    This method delete the edge from the graph.
    the method returns False if node_id1 or node_id2 aren't in the graph
    or there is no edge between them.
    if node_id1 node and node_id2 node are neighbors the method removes the edge
    between them by removing each Node from the list of neighbors [dict] of
    the other one. afterwards the method update 'edge_size' variable used for
    counting the edges and also update the MC (Mode Count).
    finally the method returns True.
    """
    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if not self.graph.__contains__(node_id1) or not self.graph.__contains__(node_id2) \
                or not self.ni.get(node_id1).__contains__(node_id2):
            return False
        self.edge_size = self.edge_size - 1
        self.revers_ni.get(node_id2).pop(node_id1)
        self.mc = self.mc + 1
        self.ni.get(node_id1).pop(node_id2)
        return True

    """
    This method prints objects of this class in the requested format.
    """
    def __repr__(self):
        return 'Graph: |V|={0} , |E|={1}'.format(len(self.graph), self.edge_size)

    """
    This method used to check equals between
    objects of this class by comparing the variables.
    """
    def __eq__(self, other):
        if not isinstance(other, DiGraph):
            return NotImplemented
        if self.edge_size != other.edge_size:
            return False
        return self.graph == other.graph and self.ni == other.ni and self.revers_ni == other.revers_ni


class NodeData:
    def __init__(self, key: int = -1, pos: tuple = None, tag: int = 0):
        self.pos = pos
        self.key = key
        self.tag = tag
        self.graph: DiGraph = None

    """
    This method implements a comparison of objects of this class type.
    mainly for the purpose of implementing the shortest_path method.
    """
    def __lt__(self, other):
        return self.tag < other.tag

    """
    This method prints objects of this class in the requested format.
    """
    def __repr__(self, g: DiGraph = None):
        if self.graph is not None and self.graph.graph.__contains__(self.key):
            return "{0}: |edges out| {1} |edges in| {2}".format(self.key,
                                                                len(self.graph.all_out_edges_of_node(self.key)),
                                                                len(self.graph.all_in_edges_of_node(self.key)))
        return "'{0}'".format(self.key)

    """
    This method is a hash method for the purpose of
    implementing the equals method in this class.
    """
    def __hash__(self):
        return hash((self.pos, self.key, self.tag))

    """
    This method used to check equals between
    objects of this class by comparing the variables.
    """
    def __eq__(self, other):
        if not isinstance(other, NodeData):
            return NotImplemented
        return self.pos == other.pos and self.key == other.key and self.tag == other.tag
