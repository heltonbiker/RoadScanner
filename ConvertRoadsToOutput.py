#!/usr/bin/env python
# coding: utf-8

import networkx as nx
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt
import time
import json

with open('nodes.txt') as nodesfile:
    nodes = [(map(int, l.split(';'))) for l in nodesfile]
    nodesdict = {node[0] : (node[1], node[2]) for node in nodes}

with open('edges.txt') as edgesfile:
    edges = [map(lambda x: nodesdict[int(x)], line.split(';')) for line in edgesfile]

graph = nx.Graph()
graph.add_edges_from(edges)

timestamp = int(time.time()*1e3)
fname = "output/{} roadgraph.json".format(timestamp)
with open(fname, 'w') as graphfile:
    json.dump(json_graph.node_link_data(graph), graphfile)
