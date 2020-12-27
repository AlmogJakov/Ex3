from GraphInterface import GraphInterface
from src.NodeData import NodeData


class DiGraph(GraphInterface):
    def __init__(self):
        self._graph = {}  # key = node key. value = node object
        self._ni = {}  # key = node key. value = node neighbors dictionaries -> key = neighbor-key. value = weight
        self._niRevers = {}  # key = node key. value = node neighbors keys (reversed) [tuple]
        self._edgeSize = 0
        self._mc = 0

    def v_size(self) -> int:
        return len(self._graph)

    def e_size(self) -> int:
        return self._edgeSize

    def get_mc(self) -> int:
        return self._mc

    def get_all_v(self) -> dict:
        return self._graph

    def all_in_edges_of_node(self, id1: int) -> dict:
        return self._ni.get(id1)

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if not self._graph.__contains__(id1) or not self._graph.__contains__(id2) or weight < 0 or id1 == id2:
            return
        if self._ni.get(id1).__contains__(id2):
            if self._graph.get(id1).get(id2) == weight:
                return
                self._graph.get(id1).update({id2: weight})
        else:
            self._graph.get(id1).update({id2: weight})
            self._niRevers.get(id2).append(id1)
            self._edgeSize = self._edgeSize + 1
        self._mc = self._mc + 1

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if self._graph.__contains__(node_id):
            return False
        new_node = NodeData()
        new_node.key = node_id
        node_id.pos = pos
        self._graph.update({node_id: new_node})
        return True

    def remove_node(self, node_id: int) -> bool:
        if not self._graph.__contains__(node_id):
            return False
        for node in self._ni.get(node_id).keys():
            self._niRevers.get(node).remove(node_id)
        ni_size = len(self._ni.get(node_id))
        self._ni.pop(node_id)
        self._edgeSize = self._edgeSize - ni_size
        self._mc = self._mc + ni_size
        self._edgeSize = self._edgeSize - len(self._niRevers.get(node_id))
        for node in self._niRevers.get(node_id):
            self._ni.get(node).pop(node_id)
            self._mc = self._mc + 1
        self._mc = self._mc + 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if not self._graph.__contains__(node_id1) or not self._graph.__contains__(node_id2)\
                or not self._ni.get(node_id1).__contains__(node_id2):
            return False
        self._edgeSize = self._edgeSize - 1
        self._niRevers.get(node_id2).remove(node_id1)
        self._mc = self._mc + 1
        self._ni.get(node_id1).pop(node_id2)
        return True
