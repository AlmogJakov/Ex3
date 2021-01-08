import timeit
import unittest
from DiGraph import DiGraph
from random import randrange

from GraphAlgo import GraphAlgo


def create_graph() -> DiGraph():
    graph = DiGraph()
    graph_algo = GraphAlgo(graph)
    for i in range(80):
        graph.add_node(i)
    for i in range(300):   # for i in (number+2000 for number in range(3000000)):
        src = randrange(100)
        dst = randrange(100)
        weight = randrange(100)
        graph.add_edge(src, dst, weight)
    return graph


class TestDiGraph(unittest.TestCase):
    def test_runtime(self):
        start = timeit.default_timer()
        graph = create_graph()
        stop = timeit.default_timer()
        print('Time to build the graph: ', stop - start)
        graph_algo = GraphAlgo(graph)
        start = timeit.default_timer()
        connected_components = graph_algo.connected_components()
        stop = timeit.default_timer()
        nodes_sum = 0
        for group in connected_components:
            nodes_sum += len(group)
        print('Time to connected_components: ', stop - start)
        print('Number of connected_components: ', len(connected_components))
        print('Sum of connected_components: ', nodes_sum)
        graph_algo.plot_graph()

if __name__ == '__main__':
    unittest.main()
