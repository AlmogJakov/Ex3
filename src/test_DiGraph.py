import unittest
from DiGraph import DiGraph, NodeData


def create_graph() -> DiGraph():
    graph = DiGraph()
    graph.add_node(0)
    graph.add_node(1)
    graph.add_node(2)
    graph.add_node(3)
    graph.add_node(4)
    graph.add_node(5)
    graph.add_node(6)
    graph.add_node(7)
    graph.add_node(8)
    graph.add_node(9)
    graph.add_node(10)
    graph.add_node(11)
    graph.add_node(12)
    graph.add_node(13)
    graph.add_node(14)
    graph.add_edge(1, 2, 0)
    graph.add_edge(2, 3, 4)
    graph.add_edge(3, 7, 9)
    graph.add_edge(7, 4, 7)
    graph.add_edge(4, 5, 5)
    graph.add_edge(5, 4, 6)
    graph.add_edge(5, 6, 2)
    graph.add_edge(6, 7, 15)
    graph.add_edge(7, 9, 2)
    graph.add_edge(9, 8, 1)
    graph.add_edge(8, 1, 3)
    graph.add_edge(10, 11, 7.5)
    graph.add_edge(10, 12, 0)
    graph.add_edge(11, 13, 0)
    graph.add_edge(12, 13, 0)
    graph.add_edge(9, 14, 3)
    #
    # Graph illustration:
    #
    #   (0)
    #                w=0
    #   (1)>------>-------->----->(2)
    #    ^           w=2           \>
    #    |      (5)>----->(6)        \
    #    |      ^   >        >        \
    #    ^      |    \        \        \
    #    |      |  w=6\    w=15\     w=4\
    #    |   w=5|      \        \        |
    # w=3|      |       \>       \>      >(3)
    #    |      ^-<-----<(4)<----<(7)<-----<
    #    |         w=5       w=7  \>   w=9
    #    ^                         \
    #    |                       w=2\
    #    |                           \>
    #    |--------<------<(8)<----<---(9)----->(14)
    #            w=3            w=1       w=3
    #
    #  	      w=7.5
    #  	(10)>-------->(11)
    #  	 >             |
    # w=0|             |w=0
    # 	 |             >
    # 	(12)>-------->(13)
    # 	       w=0
    #
    return graph


class TestDiGraph(unittest.TestCase):
    def test_v_size(self):
        graph = create_graph()
        self.assertEqual(graph.v_size(), 15)
        graph.remove_node(5)
        self.assertEqual(graph.v_size(), 14)
        graph = DiGraph()
        self.assertEqual(graph.v_size(), 0)

    def test_e_size(self):
        graph = create_graph()
        self.assertEqual(graph.e_size(), 16)
        graph.remove_edge(0, 0)
        self.assertEqual(graph.e_size(), 16)
        graph.remove_node(5)
        self.assertEqual(graph.e_size(), 13)
        graph.remove_edge(6, 7)
        self.assertEqual(graph.e_size(), 12)
        graph.remove_edge(16, 7)
        self.assertEqual(graph.e_size(), 12)

    def test_get_mc(self):
        graph = create_graph()
        self.assertEqual(graph.mc, 31)
        graph.add_node(5)
        self.assertEqual(graph.mc, 31)
        graph.remove_node(5)
        self.assertEqual(graph.mc, 35)
        graph.add_edge(6, 7, 15)
        self.assertEqual(graph.mc, 35)
        graph.remove_edge(6, 7)
        self.assertEqual(graph.mc, 36)

    def test_get_all_v(self):
        expected = {}
        graph = DiGraph()
        self.assertEqual(graph.get_all_v(), expected)
        graph = create_graph()
        self.assertEqual(len(graph.get_all_v()), 15)
        for i in range(15):
            self.assertIsInstance(graph.get_all_v().get(i), NodeData)
        pass

    def test_all_in_edges_of_node(self):
        graph = create_graph()
        self.assertEqual(graph.all_in_edges_of_node(5), {4: 5})
        self.assertEqual(graph.all_in_edges_of_node(7), {3: 9, 6: 15})
        self.assertEqual(graph.all_in_edges_of_node(11), {10: 7.5})
        self.assertEqual(graph.all_in_edges_of_node(0), {})

    def test_all_out_edges_of_node(self):
        graph = create_graph()
        self.assertEqual(graph.all_out_edges_of_node(5), {4: 6, 6: 2})
        self.assertEqual(graph.all_out_edges_of_node(7), {4: 7, 9: 2})
        self.assertEqual(graph.all_out_edges_of_node(10), {11: 7.5, 12: 0})
        self.assertEqual(graph.all_out_edges_of_node(0), {})

    def test_add_edge(self):
        graph = create_graph()
        self.assertEqual(graph.e_size(), 16)
        self.assertEqual(graph.mc, 31)
        graph.add_edge(0, 0, 0)
        self.assertEqual(graph.e_size(), 16)
        self.assertEqual(graph.mc, 31)
        graph.add_edge(9, 14, 3)
        self.assertEqual(graph.e_size(), 16)
        self.assertEqual(graph.mc, 31)
        graph.add_edge(20, 14, 0)
        graph.add_edge(9, 20, 0)
        self.assertEqual(graph.e_size(), 16)
        self.assertEqual(graph.mc, 31)
        graph.add_edge(9, 14, 4)
        self.assertEqual(graph.e_size(), 16)
        self.assertEqual(graph.mc, 32)
        graph.add_edge(1, 4, -1)
        self.assertEqual(graph.e_size(), 16)
        self.assertEqual(graph.mc, 32)
        graph.add_edge(1, 4, 2)
        self.assertEqual(graph.e_size(), 17)
        self.assertEqual(graph.mc, 33)

    def test_add_node(self):
        graph = create_graph()
        self.assertEqual(graph.v_size(), 15)
        self.assertEqual(graph.mc, 31)
        graph.add_node(0)
        self.assertEqual(graph.v_size(), 15)
        self.assertEqual(graph.mc, 31)
        graph.add_node(15)
        self.assertEqual(graph.v_size(), 16)
        self.assertEqual(graph.mc, 32)

    def test_remove_node(self):
        graph = create_graph()
        self.assertEqual(graph.v_size(), 15)
        self.assertEqual(graph.mc, 31)
        graph.remove_node(15)
        self.assertEqual(graph.v_size(), 15)
        self.assertEqual(graph.mc, 31)
        graph.remove_node(0)
        self.assertEqual(graph.v_size(), 14)
        self.assertEqual(graph.mc, 32)

    def test_remove_edge(self):
        graph = create_graph()
        self.assertEqual(graph.e_size(), 16)
        self.assertEqual(graph.mc, 31)
        graph.remove_edge(0, 0)
        graph.remove_edge(0, 1)
        graph.remove_edge(1, 0)
        self.assertEqual(graph.e_size(), 16)
        self.assertEqual(graph.mc, 31)
        graph.remove_edge(20, 0)
        graph.remove_edge(0, 20)
        graph.remove_edge(11, 10)
        self.assertEqual(graph.e_size(), 16)
        self.assertEqual(graph.mc, 31)
        graph.remove_edge(10, 11)
        self.assertEqual(graph.e_size(), 15)
        self.assertEqual(graph.mc, 32)


if __name__ == '__main__':
    unittest.main()
