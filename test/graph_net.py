import json

import matplotlib.pyplot as plt
import networkx as nx
from networkx import shortest_path, shortest_path_length

file_name = '../data/A5'
load_file = open(file_name, 'r')
graph_dict = json.loads(load_file.read())
dg = nx.DiGraph()

for n in graph_dict["Nodes"]:
    dg.add_node(n["id"])

for e in graph_dict["Edges"]:
    dg.add_edge(e["src"], e["dest"], weight=e["w"])

dg.remove_edge(13, 14)

nx.draw(dg, with_labels=True, edge_color="r")
t2 = nx.dijkstra_path(dg, 0, 3)
print(t2)
d = 0
for i in range(len(t2) - 1):
    d += dg[t2[i]][t2[i + 1]]['weight']
print(d)

t2 = nx.dijkstra_path(dg, 12, 13)
print(t2)
d = 0
for i in range(len(t2) - 1):
    d += dg[t2[i]][t2[i + 1]]['weight']
print(d)

largest = list(nx.strongly_connected_components(dg))
print(largest)

t3 = nx.strongly_connected_components(dg)
print(t3)
# nx.node_connected_component()
# plt.show()
