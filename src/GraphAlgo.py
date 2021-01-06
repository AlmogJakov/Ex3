import math
from typing import List
from queue import PriorityQueue
from GraphAlgoInterface import GraphAlgoInterface
from GraphInterface import GraphInterface
from DiGraph import DiGraph, NodeData
import matplotlib.pyplot as plt
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
            load_file.close()
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
            return float('inf'), []  # -1, None
        path_list = list()
        if id1 == id2:
            path_list.append(id1)
            return 0, path_list
        path_len, path_dict = self.dijkstra(id1, id2, {})
        if path_dict is None:
            return float('inf'), [] # -1, None
        src_node = self.DiGraph.graph.get(id1)
        dst_node = self.DiGraph.graph.get(id2)
        node_pointer = dst_node
        path_list.append(node_pointer.key)
        while True:
            node_pointer = path_dict.get(node_pointer)
            path_list.append(node_pointer.key)
            if node_pointer == src_node:
                break
        path_list.reverse()
        return path_len, path_list

    def connected_component(self, id1: int) -> list:
        if self.DiGraph is None or not self.DiGraph.graph.__contains__(id1):
            return []
        return self.find_group(id1, set())

    def connected_components(self) -> List[list]:
        if self.DiGraph is None:
            return []
        all_group = list()
        vis = set()
        for n1 in self.DiGraph.get_all_v():
            if n1 not in vis:
                group = self.find_group(n1, vis)
                all_group.append(group)
        return all_group

    def plot_graph(self) -> None:
        nodes = self.DiGraph.get_all_v()
        has_pos = False
        has_not_pos = False

        if len(nodes) == 0:  # the graph is empty
            plt.axes()
            plt.show()
            return None

        x_val = []
        y_val = []
        id_n = []
        node_without_pos = set()

        for i in nodes.values():
            if i.pos is not None:
                x_val.append(i.pos[0])
                y_val.append(i.pos[1])
                id_n.append(i.key)
                has_pos = True
            else:
                node_without_pos.add(i.key)
                has_not_pos = True

        if has_pos and not has_not_pos:
            self.print_graph(x_val, y_val, id_n)
        else:
            if has_pos:
                max_x, max_y = max(x_val), max(y_val)
                min_x, min_y = min(x_val), min(y_val)
                mid = ((max_x + min_x) / 2, (max_y + min_y) / 2)
                radios = (((max_x - min_x) * 1.1) ** 2 + ((max_y - min_y) * 1.1) ** 2) ** 0.5 / 2
            else:
                mid = (2, 2)
                radios = 1

            alpha = 360 / len(node_without_pos)
            list_nodes = self.connected_components()
            i = 0

            # add position to nodes without position
            for group in list_nodes:
                for n in group:
                    if node_without_pos.__contains__(n):
                        id_n.append(n)
                        x = (radios * math.sin(math.radians(i * alpha))) + mid[0]
                        x_val.append(x)
                        y = (radios * math.cos(math.radians(i * alpha))) + mid[1]
                        y_val.append(y)
                        i += 1
            self.print_graph(x_val, y_val, id_n)
            return None

    def print_graph(self, x_val, y_val, id_n):
        ax = plt.axes()
        nodes = self.DiGraph.get_all_v()
        ax.plot(x_val, y_val, "-Dy")

        for i in range(len(id_n)):
            ax.text(x_val[i], y_val[i], id_n[i], fontsize=8, color='blue', ha='center')

        ed = []
        for key1, n in nodes.items():
            for key2 in self.DiGraph.all_out_edges_of_node(key1):
                i1 = id_n.index(key1)
                i2 = id_n.index(key2)
                a = (key1, (x_val[i1], y_val[i1]), (x_val[i2], y_val[i2]))
                ed.append(a)

        for n, src, dest in ed:
            ax.annotate('', xy=(float(dest[0]), float(dest[1])), xytext=(float(src[0]), float(src[1])), ha='center',
                        arrowprops={'arrowstyle': '->'})
        plt.show()

    def dijkstra(self, src, dst, the_path) -> (float, dict):
        pq = PriorityQueue()
        # node that we already check
        ch = {}  # key=int, val=node_data
        flag = False
        node_src = self.DiGraph.graph.get(src)
        node_src.tag = 0
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
                            n2.tag = -1
                        n2.tag = w_key1 + w
                        ch.update({key2: n2})
                        the_path.update({n2: n1})
                        pq.put(n2)
        if flag:
            return ch.get(dst).tag, the_path
        return -1, None

    def find_group(self, id1: int, vis: set) -> list:
        group = list()
        ni1 = self.is_connected_bfs(id1, self.DiGraph.ni)
        ni2 = self.is_connected_bfs(id1, self.DiGraph.revers_ni)
        for n1 in ni1:
            if ni2.__contains__(n1):
                group.append(n1.key)
                vis.add(n1.key)
        group.sort()
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

    def __eq__(self, other):
        if not isinstance(other, GraphAlgo):
            return NotImplemented
        return self.DiGraph == other.DiGraph
