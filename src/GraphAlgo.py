from typing import List
from queue import PriorityQueue
from GraphAlgoInterface import GraphAlgoInterface
from GraphInterface import GraphInterface
from DiGraph import DiGraph, NodeData
import json
import queue
import logging


class GraphAlgo(GraphAlgoInterface):
    def __init__(self, g: DiGraph = DiGraph()):
        self.DiGraph = g

    def get_graph(self) -> GraphInterface:
        return self.DiGraph

    def load_from_json(self, file_name: str) -> bool:
        try:
            g = DiGraph()
            load_file = open(file_name, 'r')
            graph_dict = json.loads(load_file.read())
            edges = graph_dict["Edges"]
            nodes = graph_dict["Nodes"]
            # add the nodes
            for n in nodes:
                id_n = n["id"]
                if n.__contains__("pos"):
                    pos_val = n["pos"].split(',')
                    pos_n = (float(pos_val[0]), float(pos_val[1]), float(pos_val[2]))
                    g.add_node(id_n, pos_n)
                else:
                    g.add_node(id_n, None)
            # add the edges
            for ed in edges:
                g.add_edge(ed['src'], ed['dest'], ed['w'])
            self.DiGraph = g
            return True
        except Exception as e:
            logging.error('Failed.', exc_info=e)
            return False

    def save_to_json(self, file_name: str) -> bool:
        try:
            g = {"Edges": [], "Nodes": []}
            nodes = self.DiGraph.get_all_v()
            for n in nodes:
                edges = self.DiGraph.all_out_edges_of_node(n)
                for ed in edges:
                    g["Edges"].append({"src": n, "w": edges[ed], "dest": ed})
                pos = nodes[n].pos
                if pos is None:
                    g["Nodes"].append({"id": n})
                else:
                    pos_str = str(pos[0]) + "," + str(pos[1]) + "," + str(pos[2])
                    g["Nodes"].append({"pos": pos_str, "id": n})
            with open(file_name, 'w') as outfile:
                json.dump(g, outfile)
            return True
        except Exception as e:
            logging.error('Failed.', exc_info=e)
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        if not self.DiGraph.graph.__contains__(id1) or not self.DiGraph.graph.__contains__(id2):
            return -1, None
        path_list = list()
        if id1 == id2:
            path_list.append(self.DiGraph.graph.get(id1))
            return 0, path_list
        path_len, path_dict = self.dijkstra(id1, id2, {})
        if path_dict is None:
            return -1, None
        src_node = self.DiGraph.graph.get(id1)
        dst_node = self.DiGraph.graph.get(id2)
        node_pointer = dst_node
        path_list.append(node_pointer)
        while True:
            node_pointer = path_dict.get(node_pointer)
            path_list.append(node_pointer)
            if node_pointer == src_node:
                break
        path_list.reverse()
        return path_len, path_list

    def connected_component(self, id1: int) -> list:
        return self.find_group(id1, set())

    def connected_components(self) -> List[list]:
        all_group = list()
        vis = set()
        for n in self.DiGraph.get_all_v():
            if not (n in vis):
                # print(n not in vis)
                group = self.find_group(n, vis)
                all_group.append(group)
        return all_group

    def plot_graph(self) -> None:
        pass

    def dijkstra(self, src, dst, the_path) -> (float, dict):
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
            if key1 == dst:
                flag = True
            else:
                ed = self.DiGraph.all_out_edges_of_node(key1)
                for key2 in ed:
                    w = ed.get(key2)
                    n2 = self.DiGraph.graph.get(key2, NodeData())
                    w_key1 = n1.tag
                    if not ch.__contains__(key2) or ch.get(key2).tag > w_key1 + w:
                        if not ch.__contains__(key2):
                            n2.tag = 0
                        n2.tag = w_key1 + w
                        ch.update({key2: n2})
                        the_path.update({n2: n1})
                        pq.put(n2)
        if flag:
            return ch.get(dst).tag - 1, the_path
        return -1, None

    def find_group(self, id1: int, vis: set) -> list:
        group = list()
        ni1 = self.is_connected_bfs(id1, self.DiGraph.ni)
        ni2 = self.is_connected_bfs(id1, self.DiGraph.revers_ni)
        for n1 in ni1:
            if ni2.__contains__(n1):
                group.append(n1)
                vis.add(n1)
        return group

    def is_connected_bfs(self, src: int, ni: dict) -> set:
        vis = set()
        q = queue.Queue()
        current = self.DiGraph.graph.get(src)
        vis.add(current)
        q.put(current)
        while not q.empty():
            current = q.get()
            for ed in ni.get(current.key):
                n = self.DiGraph.graph.get(ed)
                if not vis.__contains__(n):
                    q.put(n)
                    vis.add(n)
        return vis
