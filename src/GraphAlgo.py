from typing import List
from queue import PriorityQueue

from GraphAlgoInterface import GraphAlgoInterface
from GraphInterface import GraphInterface
from DiGraph import DiGraph


class GraphAlgo(GraphAlgoInterface):
    def __init__(self, g: DiGraph = DiGraph()):
        self.DiGraph = g

    def get_graph(self) -> GraphInterface:
        return self.DiGraph

    def load_from_json(self, file_name: str) -> bool:
        pass

    def save_to_json(self, file_name: str) -> bool:
        pass

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        pass

    def connected_component(self, id1: int) -> list:
        pass

    def connected_components(self) -> List[list]:
        pass

    def plot_graph(self) -> None:
        pass

    def dijkstra(self, src, dest, the_path):
        pq = PriorityQueue()
        # node that we already check
        ch = {}  # key=int, val=node_data
        flag = False
        node_src = self.DiGraph.graph.get(src)
        node_src.tag = 1
        pq.put(node_src)
        ch.update({src: node_src})
        while not pq.empty() and not flag:
            n1 = pq.get()
            key1 = n1.key
            if key1 == dest:
                flag = True
            else:
                ed = self.DiGraph.all_out_edges_of_node(key1)
                for key2 in ed:
                    w = ed.get(key2)
                    n2 = self.DiGraph.graph.get(key2)
                    w_key1 = n1.tag
                    if not ch.__contains__(key2) or ch.get(key2).tag > w_key1 + w:
                        ch.update({key2: n2})
                        the_path.update({n2,n1})
                        pq.put(n2)
        if flag:
            return ch.get(dest).tag - 1
        return -1