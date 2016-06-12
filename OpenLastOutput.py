#!/usr/bin/env python
# coding: utf-8

import json
import glob

import networkx as nx
from networkx.readwrite import json_graph

import matplotlib.pyplot as plt


lastfile = sorted(glob.glob('output/*.json'))[-1]
with open(lastfile) as jsonfile:
    jsondict = json.load(jsonfile)

nodes = [tuple(node['id']) for node in jsondict['nodes']]
edges = [(nodes[edge['source']], nodes[edge['target']]) for edge in jsondict['links']]

G = nx.Graph()
G.add_edges_from(edges)

for node in G.nodes():
    if nx.degree(G, node) < 2:
        G.remove_node(node)

intersections = [node for node in G.nodes() if nx.degree(G, node) > 2]

for edge in G.edges():
    lons, lats = zip(*edge)
    plt.plot(lons, lats, c="g", lw=3, alpha=0.5, zorder=1)

# lons, lats = zip(*G.nodes())
# plt.scatter(lons, lats, c='b', linewidths=0, zorder=2)

lons, lats = zip(*intersections)
plt.scatter(lons, lats, s=70, linewidths=0, c='r', zorder=3)


plt.axis('equal')
plt.show()