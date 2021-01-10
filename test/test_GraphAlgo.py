import unittest
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo
import test_DiGraph


class TestGraphAlgo(unittest.TestCase):
    def test_get_graph(self):
        graph_algo = GraphAlgo()
        self.assertEqual(graph_algo, GraphAlgo())
        graph_algo = GraphAlgo(test_DiGraph.create_graph())
        self.assertEqual(graph_algo.get_graph(), test_DiGraph.create_graph())

    def test_shortest_path(self):
        graph = test_DiGraph.create_graph()
        graph_algo = GraphAlgo(graph)
        self.assertEqual(graph_algo.shortest_path(1, 7)[0], 13)
        self.assertEqual(graph_algo.shortest_path(1, 10)[0], float('inf'))
        self.assertEqual(graph_algo.shortest_path(10, 13)[0], 0)
        self.assertEqual(graph_algo.shortest_path(7, 6)[0], 14)
        self.assertEqual(graph_algo.shortest_path(10, 11)[0], 7.5)
        result = None
        directions = graph_algo.shortest_path(1, 7)[1]
        if directions is not None:
            result = ""
            for n in directions:
                result = result + str(n) + ", "
        # print(result)
        self.assertEqual(result, "1, 2, 3, 7, ")
        expected = []
        directions = graph_algo.shortest_path(1, 10)[1]
        self.assertEqual(expected, directions)
        expected = []
        directions = graph_algo.shortest_path(14, 9)[1]
        self.assertEqual(expected, directions)
        result = None
        directions = graph_algo.shortest_path(10, 13)[1]
        if directions is not None:
            result = ""
            for n in directions:
                result = result + str(n) + ", "
        # print(result)
        self.assertEqual(result, "10, 12, 13, ")
        result = None
        directions = graph_algo.shortest_path(7, 6)[1]
        if directions is not None:
            result = ""
            for n in directions:
                result = result + str(n) + ", "
        # print(result)
        self.assertEqual(result, "7, 4, 5, 6, ")

    def test_save_and_load_from_json(self):
        g = DiGraph()
        g.add_node(0, (0, 1, 2))
        g.add_node(1, (3, 4, 5))
        g.add_node(2, (6, 7, 8))
        g.add_node(3, (7, 6, 5))
        for i in range(3):
            g.add_edge(i, i + 1, i + 2)
        ga_original = GraphAlgo(g)
        ga_original.save_to_json("check_file")
        ga_loaded = GraphAlgo()
        returned_bool = ga_loaded.load_from_json("check_file")
        self.assertTrue(returned_bool)
        self.assertEqual(ga_original, ga_loaded)
        ga_original.DiGraph.graph.get(0).pos = (0, 1.1, 2)
        self.assertNotEqual(ga_original, ga_loaded)
        ga_original.DiGraph.graph.get(0).pos = (0, 1, 2)
        self.assertEqual(ga_original, ga_loaded)
        ga_original.DiGraph.remove_edge(0, 1)
        self.assertNotEqual(ga_original, ga_loaded)
        self.assertEqual(False, ga_original.load_from_json("non_existing_graph"))

    def test_connected_component(self):
        graph = test_DiGraph.create_graph()
        graph_algo = GraphAlgo(graph)
        self.assertEqual(graph_algo.connected_component(0), [0])
        self.assertEqual(graph_algo.connected_component(7), [1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(graph_algo.connected_component(10), [10])
        self.assertEqual(graph_algo.connected_component(20), [])

    def test_connected_components(self):
        graph_algo = GraphAlgo()
        self.assertEqual(graph_algo.connected_components(), [])
        graph = test_DiGraph.create_graph()
        graph_algo = GraphAlgo(graph)
        self.assertEqual(graph_algo.connected_components(), [[0], [1, 2, 3, 4, 5, 6, 7, 8, 9],
                                                             [10], [11], [12], [13], [14]])


if __name__ == '__main__':
    unittest.main()
