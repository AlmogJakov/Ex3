import json
import timeit
import unittest
from asyncio import sleep

import networkx as nx

from src.GraphAlgo import GraphAlgo


def load_to_nx(file_name):
    load_file = open(file_name, 'r')
    graph_dict = json.loads(load_file.read())
    dg = nx.DiGraph()

    for n in graph_dict["Nodes"]:
        dg.add_node(n["id"])

    for e in graph_dict["Edges"]:
        dg.add_edge(e["src"], e["dest"], weight=e["w"])
    return dg


def check(file_name):
    print(" * My graph *")

    ga = GraphAlgo()
    ga.load_from_json(file_name)

    # connected_components function
    start = timeit.default_timer()
    gc = ga.connected_components()
    stop = timeit.default_timer()
    print('Time for connected_components function: ', stop - start)

    max_connected = max(gc, key=len)
    min_id = min(max_connected)

    final_list = []
    shortest_list = []
    shortest_list_nx = []
    t = 5

    for i in range(0, t):
        max_1 = max(max_connected)
        final_list.append(max_1)
        max_connected.remove(max_1)

    # shortest_path function
    start = timeit.default_timer()
    for i in final_list:
        shortest_list.append(ga.shortest_path(min_id, i))

    stop = timeit.default_timer()
    print('Time for shortest_path function: ', (stop - start) / 5)

    # connected_component function
    start = timeit.default_timer()
    for i in final_list:
        ga.connected_component(i)

    stop = timeit.default_timer()
    print('Time for connected_component function: ', (stop - start) / 5)

    # ========================
    # ==== NetworkX graph ====
    # ========================
    print("\n * networkx graph *")
    graph_nx = load_to_nx(file_name)

    # connected_components function
    start = timeit.default_timer()
    gcn = list(nx.strongly_connected_components(graph_nx))
    stop = timeit.default_timer()
    print('Time for connected_components function: ', stop - start)

    # shortest_path function
    start = timeit.default_timer()
    for i in final_list:
        shortest_list_nx.append(nx.dijkstra_path(graph_nx, min_id, i))

    stop = timeit.default_timer()
    print('Time for shortest_path function: ', (stop - start) / 5)

    b = True

    if not len(gc) == len(gcn):
        b = False

    for i in range(t):
        for i1 in shortest_list_nx:
            d = 0
            for i2 in range(len(i1) - 1):
                d += graph_nx[i1[i2]][i1[i2 + 1]]['weight']

            if not 0.0001 > shortest_list[i][0] - d > -0.0001:
                b = True

    print("\n\nmin_id = " + str(min_id))
    print("max_connected = " + str(final_list))

    return b


class MyTestCase(unittest.TestCase):
    def test_graph_with_10_nodes(self):
        print(" ==== Graph with 10 node ====")
        file_name = '../data/G_10_80_0.json'
        b = check(file_name)
        self.assertEqual(b, True)

    def test_graph_with_100_nodes(self):
        print("\n ==== Graph with 100 node ====")
        file_name = '../data/G_100_800_0.json'
        b = check(file_name)
        self.assertEqual(b, True)

    def test_graph_with_1000_nodes(self):
        print("\n ==== Graph with 1000 node ====")
        file_name = '../data/G_1000_8000_0.json'
        b = check(file_name)
        self.assertEqual(b, True)

    def test_graph_with_10_thousand_nodes(self):
        print("\n ==== Graph with 10 thousand node ====")
        file_name = '../data/G_10000_80000_0.json'
        b = check(file_name)
        self.assertEqual(b, True)

    def test_graph_with_20_thousand_nodes(self):
        print("\n ==== Graph with 20 thousand node ====")
        file_name = '../data/G_20000_160000_0.json'
        b = check(file_name)
        self.assertEqual(b, True)

    def test_graph_with_30_thousand_nodes(self):
        print("\n ==== Graph with 30 thousand node ====")
        file_name = '../data/G_30000_240000_0.json'
        b = check(file_name)
        self.assertEqual(b, True)


if __name__ == '__main__':
    unittest.main()
