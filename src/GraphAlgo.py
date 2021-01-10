import math
from typing import List
from queue import PriorityQueue
from src.GraphAlgoInterface import GraphAlgoInterface
from src.GraphInterface import GraphInterface
from src.DiGraph import DiGraph
import matplotlib.pyplot as plt
import json
import queue


# import logging


class GraphAlgo(GraphAlgoInterface):
    def __init__(self, g: DiGraph = DiGraph()):
        self.DiGraph = g

    """
    This method returns the underlying graph of which this class works.
    """

    def get_graph(self) -> GraphInterface:
        return self.DiGraph

    """
    This method load a graph to this graph
    algorithm. if the file was successfully loaded - the underlying graph of this
    class will be changed (to the loaded one), in case the graph was not loaded
    the original graph remain "as is". this method returns true - iff the graph
    was successfully loaded.
    """

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
        except IOError:
            return False
        # except Exception as e:
        #     logging.error('Failed.', exc_info=e)
        #     return False

    """
    This method saves this weighted directed
    graph to the given file name in json format.
    the method returns true - iff the file was successfully saved.
    """

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
        except IOError:
            return False
        # except Exception as e:
        #     logging.error('Failed.', exc_info=e)
        #     return False

    """
    This method returns the shortest path (by weight).
    in this method we using the algo dijkstra() that returns the shortest path distance.
    the method returns the length and the path of the shortest path between src to dst
    """

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        if not self.DiGraph.graph.__contains__(id1) or not self.DiGraph.graph.__contains__(id2):
            return float('inf'), []  # -1, None
        path_list = list()
        if id1 == id2:
            path_list.append(id1)
            return 0, path_list
        path_len, path_dict = self.dijkstra(id1, id2, {})
        if path_dict is None:
            return float('inf'), []  # -1, None
        src_node = id1
        dst_node = id2
        node_pointer = dst_node
        path_list.append(node_pointer)
        while True:
            node_pointer = path_dict.get(node_pointer)
            path_list.append(node_pointer)
            if node_pointer == src_node:
                break
        path_list.reverse()
        return path_len, path_list

    """
          This method returns a list of all the connected component of the key 'id1' using twice the BFS algorithm.
          In this method we call to method find_graph() that using tow list,ni1 and ni2.
          List ni1 get the weakly connection, all in edges of id1
          List ni2 get the weakly connection, all out edges of id1
          Then find the nodes that are in both and that is connected component of the key
          the method returns a list of all the connected component of the key
    """

    def connected_component(self, id1: int) -> list:
        if self.DiGraph is None or not self.DiGraph.graph.__contains__(id1):
            return []
        return self.find_group(id1, set())

    """
          This method returns a list of list of all the connected components in the graph.
          In this method we call to method find_graph() we send vis that mark the node 
          that already have a connected component and return all the connected components in the graph.
    """

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

    """
           This method upload a position to the nodes and send them to print_graph().
           First we put on the lists x_val, y_val, id_n, the position of the node that already have position.
           If all the nodes have position the function send them straight to the method print_graph()
           that print all the graph by using matplotlib library.
           If there are nodes that has position and there are nodes with no position:
              [+] we take tow points:
                1. (x,y) - x is the max of the list x_val, y is the max of the list y_val.
                2. (x,y) - x is the min of the list x_val, y is the min of the list y_val.
              [+] Then we fine the middle between them:
                mid(x,y) - x = (max_x + min_x)/2, y = (max_y + min_y)/2.
              [+] Finally we find the radios of the circle:
                radios = (((max_x - min_x)*1.1)^2 + ((max_y - min_y)*1.1)^2)^0.5 / 2
                     (We multiply with 1.1 to increase the circle that there will be no collision of nodes) 
           If there aren't nodes that has position and there are nodes with no position:
              [+] We choose mid:
                 mid(x,y) = (2,2).
              [+] we choose radios:
                 radios = 1.      
           After we find the mid point and the radios now we find the alpha:
              alpha = 360 / n .(n - number of the nodes that without position)
           Then we can calculate the position of each nodes that without position:
              For each point without location:
                  x = (radios * sin(i * alpha) + mid[x]
                  y = (radios * cos(i * alpha) + mid[y]
                  ('i' is resized every time by 1 that for place the nodes evenly)  
           Finally we send the the lists x_val, y_val, id_n, to the method print_graph().       
    """

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

    """
       This method print the graph by using the library matplotlib.
       We get the lists x_val, y_val, id_n, that present the position of the node in the graph.
       Function 'ax.plot(x_val, y_val, "Dy")' we print on the graph squares at the position 
       of the nodes.
       List ed[] keep the trio (id of the node, pos of the node, pos of the node that the edge go to)
       With function ax.annotate() we use the list ed[] to print the arrow. 
    """

    def print_graph(self, x_val, y_val, id_n):
        ax = plt.axes()
        nodes = self.DiGraph.get_all_v()
        ax.plot(x_val, y_val, "Dy")

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

    """
    This is an auxiliary method method for two methods: (We implemented both of the methods in the same way)
        an method to returns the length of the shortest path between src to dst.
        an method to returns a List of the shortest path between src to dst.
     The method is based on dijkstra's algorithm.
     In this algorithm we use a couple of data structures:
        an dict to store the vertices we "visit".
        an PriorityQueue to store the the neighbors of the Node on which iterations are performed (sorted).
        an dict to store the Nodes for building the output path - each node with his parent.
     Initially we add all the Nodes to the PriorityQueue with weight = -1, and src weight = 0.
     using the dijkstra's algorithm we progress through the graph:  
        while the PriorityQueue isn't empty:
            mark the first Node on the queue (lowest weight value to source Node) as current.
            delete the current Node from the PriorityQueue.
            mark the current Node as visited (by adding the current Node to the dict).
                We loop on the neighbors of the current Node (by their weight) as long as the queue isn't empty:
                if a node that marked as visited founded  => remove from the neighbors PriorityQueue.
                else =>
                    remove from the neighbors PriorityQueue.
                    Setting variable = the weight from the current Node to the source Node.
                    update the weight of the current Node in case the variable is lower.
                    add the current Node to the dict that stores the Nodes for the output path.
                    // we store the Node as a key while his parent is the value. //
                    // that's means that through a Node we can return to his parent (progress one level) //
                    // (we need to store the shortest path = shortest levels to destination) //
                    mark the Node as visited.
     The method will stop when the PriorityQueue is empty.
     At the end of the loop:
        if the Flag == False => return null (-1 for length); // can't reach destination.
        else => do nothing. // we reached destination Node.
     Finally we build the path using the dict that stores the Nodes for the output path
     // each Node is a key while his parent is the value. (so we can build levels from dst to src). //
        start with destination Node:
            while node!=null:
                add the node to the output path List and progress to his parent through the dict.
     - for returning a List of the shortest path between src to dst:
        we reverse the List to get src->dst path instead of dst->src path.
        then we return the List as requested.
     - for returning the length of the shortest path:
        we return the tag of the dst node.
    """

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
                    n2 = self.DiGraph.graph.get(key2)
                    w_key1 = n1.tag
                    if not ch.__contains__(key2) or ch.get(key2).tag > w_key1 + w:
                        if not ch.__contains__(key2):
                            n2.tag = -1
                        n2.tag = w_key1 + w
                        ch.update({key2: n2})
                        the_path.update({n2.key: n1.key})
                        pq.put(n2)
        if flag:
            return ch.get(dst).tag, the_path
        return -1, None

    """
       This method returns a list of all the connected component of the key 'id1' using twice the BFS algorithm.
       In this method we using tow list,ni1 and ni2.
       List ni1 get the weakly connection, all in edges of id1
       List ni2 get the weakly connection, all out edges of id1
       Then find the nodes that are in both and that is connected component of the key
       the method returns a list of all the connected component of the key
    """

    def find_group(self, id1: int, vis: set) -> list:
        group = list()
        ni1 = []
        ni2 = []
        if len(self.DiGraph.ni.get(id1)) == 0 or len(self.DiGraph.revers_ni.get(id1)) == 0:
            node = self.DiGraph.graph.get(id1)
            ni1.append(node)
            ni2.append(node)
        else:
            ni1 = self.is_connected_bfs(id1, self.DiGraph.ni)
            ni2 = self.is_connected_bfs(id1, self.DiGraph.revers_ni)
        for n1 in ni1:
            if ni2.__contains__(n1):
                group.append(n1.key)
                vis.add(n1.key)
        group.sort()
        return group

    """
    This method returns a set of all the vertices connected to src node using the BFS algorithm.
    In this algorithm we use a data structure of a queue to store the vertices we "visit".
    In addition, we use a data structure of a set to store the Nodes we "visited" before.
    so that we don't loop this Nodes again.
    Initially we use an iterator on the src Node in the graph and adding the Node to the queue.
    using the BFS algorithm we progress through the neighbor list of the first Node in the queue:
    mark the first Node on the queue as current.
    delete the current Node from the queue. 
    mark the current Node as visited (by adding the current Node to the set).
    We loop on the neighbors of the current Node as long as the queue isn't empty:
            if we found a node that marked as visited => do nothing.
            else => we add the Node to the queue and mark the Node as visited.
    The method will stop when the loop "visits" all the Nodes that
    were connected to the first Node (where we started).
    the method returns a set of all the vertices we visited
    """

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

    """
    This method used to check equals between
    objects of this class by comparing the variables.
    """

    def __eq__(self, other):
        if not isinstance(other, GraphAlgo):
            return NotImplemented
        return self.DiGraph == other.DiGraph
