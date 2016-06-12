#!/usr/bin/env python
# coding: utf-8

import networkx as nx
import matplotlib.pyplot as plt

with open('nodes.txt') as nodesfile:
    nodes = [(map(int, l.split(';'))) for l in nodesfile]
    nodesdict = {node[0] : (node[1], node[2]) for node in nodes}

with open('edges.txt') as edgesfile:
    edges = [map(lambda x: nodesdict[int(x)], line.split(';')) for line in edgesfile]

graph = nx.Graph()
graph.add_edges_from(edges)

for node in graph.nodes():
    if nx.degree(graph, node) > 2:
        graph.remove_node(node)

for road in nx.connected_component_subgraphs(graph):
    
    endpoints = [n for n in road if nx.degree(graph, n) == 1]
    
    if not endpoints:
        continue

    path = nx.shortest_path(road, endpoints[0], endpoints[1])

    lons, lats = zip(*path)
    plt.plot(lons, lats)

plt.axis('equal')
plt.grid()

plt.show()














# plt.figure()
# for edge in edges:
#     lons, lats = zip(*edge)
#     plt.plot(lons, lats)

# plt.axis('equal')
# plt.grid()






# plt.figure()

# indices, lons, lats = zip(*nodes)
# plt.scatter(lons, lats, color='b', s=5, linewidths=0, alpha=0.5)

# plt.axis('equal')
# plt.grid()




# plt.show()