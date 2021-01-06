import json
import timeit
import unittest

import networkx as nx




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

    # ========================
    # ==== NetworkX graph ====
    # ========================
    print(" * networkx graph *")
    graph_nx = load_to_nx(file_name)

    # connected_components function
    start = timeit.default_timer()
    gcn = list(nx.strongly_connected_components(graph_nx))
    stop = timeit.default_timer()
    print('Time for connected_components function: ', stop - start)


    max_connected = max(gcn, key=len)
    min_id = min(max_connected)

    final_list = []
    shortest_list = []
    shortest_list_nx = []
    t = 5

    for i in range(0, t):
        max_1 = max(max_connected)
        final_list.append(max_1)
        max_connected.remove(max_1)

    print("min_id=" + str(min_id))
    print("max_connected=" + str(final_list))

    # shortest_path function
    start = timeit.default_timer()
    for i in final_list:
        shortest_list_nx.append(nx.dijkstra_path(graph_nx, min_id, i))

    stop = timeit.default_timer()
    print('Time for shortest_path function: ', (stop - start) / 5)

    return


class MyTestCase(unittest.TestCase):
    def test_graph_with_100_nodes(self):
        print(" ==== Graph with 100 node ====")
        file_name = '../data/graph_100'
        b = check(file_name)
        self.assertEqual(b, True)

    def test_graph_with_10_thousand_nodes(self):
        print("\n ==== Graph with 10 thousand node ====")
        file_name = '../data/graph_10_thousand'
        b = check(file_name)
        self.assertEqual(b, True)

    def test_graph_with_million_nodes(self):
        print("\n ==== Graph with million node ====")
        file_name = '../data/graph_million'
        b = check(file_name)
        self.assertEqual(b, True)


if __name__ == '__main__':
    unittest.main()
