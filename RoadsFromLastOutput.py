#!/usr/bin/env python
# coding: utf-8

import json
import glob
import itertools

import networkx as nx
from networkx.readwrite import json_graph

import matplotlib.pyplot as plt


lastfile = sorted(glob.glob('output/*.json'))[-1]
with open(lastfile) as jsonfile:
    jsondict = json.load(jsonfile)

nodes = [tuple(node['id']) for node in jsondict['nodes']]
edges = [(nodes[edge['source']], nodes[edge['target']]) for edge in jsondict['links']]

graph = nx.Graph()
graph.add_edges_from(edges)

roadnodes = [node for node in graph.nodes() if nx.degree(graph, node) == 2]
        
roads = []

while roadnodes:
    print len(roadnodes)
    roadnode = roadnodes.pop()

    road = []

    # take the neighbor for each side and start the road with current node
    forward, backwards = graph.neighbors(roadnode)
    road.append(roadnode)

    while True:
        road.append(forward)
        if forward in roadnodes:
            roadnodes.remove(forward)

        forward_degree = nx.degree(graph, forward)
        if forward_degree != 2:
            break
        else:
            next_forward = [neighbor for neighbor in graph.neighbors(forward) if neighbor not in road][0]
            forward = next_forward

    while True:
        road.insert(0, backwards)
        if backwards in roadnodes:
            roadnodes.remove(backwards)

        backwards_degree = nx.degree(graph, backwards)
        if backwards_degree != 2:
            break
        else:
            next_backwards = [neighbor for neighbor in graph.neighbors(backwards) if neighbor not in road][0]
            backwards = next_backwards


    # neighbors = graph.neighbors(backwards)
    # if not neighbors:
    #     road.insert(0, backwards)
    #     graph.remove_node(backwards)
    #     roadnodes.remove(backwards)

    lons, lats = zip(*road)
    plt.plot(lons, lats)

plt.axis('equal')
plt.show()



exit()





# while len(supernodes) > 0:                            # while I have supernodes to start a road
#     start = supernodes.pop()                          # take some supernode from that list
#     neighbors = graph.neighbors(start)                # check the neighbors so that I can take some path from it
#     while len(neighbors) > 0:                         # choose some neighbor so that I can start walking
#         nextNode = neighbors.pop()                    
#         road = [start, nextNode]                      # form the first segment of the road

#         lons, lats = zip(*road)
#         plt.plot(lons, lats)

#         nextNeighbors = [n for n in graph.neighbors(nextNode) if n not in neighbors]
#         print nextNeighbors



# plt.axis('equal')
# plt.show()


# exit()

for source, target in itertools.combinations(supernodes, 2):
    try:
        path = nx.shortest_path(graph, source, target)
        if len([node for node in path if nx.degree(graph,node) != 2]) == 2:
            roads.append(path)
            for node in path[1:-1]:
                graph.remove_node(node)
            print "one more"
    except Exception as e:
        pass

for road in roads:
    lons, lats = zip(*road)
    plt.plot(lons, lats, lw=3, alpha=0.5)

plt.axis('equal')
plt.show()