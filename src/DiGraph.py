from GraphInterface import GraphInterface


class DiGraph(GraphInterface):
    def __init__(self):
        self.graph = {}  # key = node key. value = node object
        self.ni = {}  # key = node key. value = (node neighbors dictionaries ->) key = neighbor-key. value = weight
        self.revers_ni = {}  # key = node key. value = tuple list of node neighbors keys (with reversed edges)
        self.edge_size = 0
        self.mc = 0

    def v_size(self) -> int:
        return len(self.graph)

    def e_size(self) -> int:
        return self.edge_size

    def get_mc(self) -> int:
        return self.mc

    def get_all_v(self) -> dict:
        return self.graph

    def all_in_edges_of_node(self, id1: int) -> dict:
        edges = {}
        for ni in self.revers_ni.get(id1):
            edges.update({ni: self.ni.get(ni).get(id1)})
        return edges

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self.ni.get(id1)

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if not self.graph.__contains__(id1) or not self.graph.__contains__(id2) or weight < 0 or id1 == id2:
            return False
        self.ni.get(id1).update({id2: weight})
        self.revers_ni.get(id2).append(id1)
        self.edge_size = self.edge_size + 1
        self.mc = self.mc + 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if self.graph.__contains__(node_id):
            return False
        new_node = NodeData()
        new_node.key = node_id
        new_node.pos = pos
        self.graph.update({node_id: new_node})
        self.ni.update({node_id: {}})
        self.revers_ni.update({node_id: list()})
        self.mc += self.mc
        return True

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
        self.mc = self.mc + 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if not self.graph.__contains__(node_id1) or not self.graph.__contains__(node_id2) \
                or not self.ni.get(node_id1).__contains__(node_id2):
            return False
        self.edge_size = self.edge_size - 1
        self.revers_ni.get(node_id2).pop(node_id1)
        self.mc = self.mc + 1
        self.ni.get(node_id1).pop(node_id2)
        return True

    def __repr__(self):
        return 'Graph: |V|={0}|, |E|={1}'.format(len(self.graph), self.edge_size)


class NodeData:
    def __init__(self, key: int = -1, pos: tuple = (0, 0, 0), tag: int = 0):
        self.pos = pos
        self.key = key
        self.tag = tag

    def __lt__(self, other):
        return self.tag < other.tag

    def __repr__(self):
        return '{0}'.format(self.key)

