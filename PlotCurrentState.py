#!/usr/bin/env python
# coding: utf-8

import json
import glob

lastfile = sorted(glob.glob('output/*.json'))[-1]
with open(lastfile) as jsonfile:
    jsondict = json.load(jsonfile)

nodes = [tuple(node['id']) for node in jsondict['nodes']]
edges = [(nodes[edge['source']], nodes[edge['target']]) for edge in jsondict['links']]

edgeDict = {}

for edge in edges:
    src, dst = edge
    for key, val in [(src, dst), (dst, src)] :
        if key in edgeDict:
            edgeDict[key].append(val)
        else:
            edgeDict[key] = ([val])


# Identify endpoint nodes: order other than 2
endpoint = []
for src, dst in edgeDict.iteritems():
    if len(dst) != 2:
        endpoint.append(src)

roads = []    # List of roads, each a list of nodes

# Build roads between the identified endpoints
# Pick the first endpoint in the remaining list.
# Move to the first-listed adjacent node.
# Keep going until we hit another node on the endpoint list.
while len(endpoint) > 0:
    here = endpoint[0]

    # Pick a first step and consume the edge
    next = edgeDict[here].pop(0)
    edgeDict[next].remove(here)
    road = [here, next]

    # If that's the last connection to the node, remove that node from the endpoints list.
    if len(edgeDict[here]) == 0:
        del endpoint[0]
        del edgeDict[here]

    # Special case for a one-segment road; endpoint entry of "next" is removed after the loop
    if next != here and len(edgeDict[next]) == 0:
        del edgeDict[next]

    # Consume edges until we reach another endpoint.
    while next not in endpoint:
        here = next
        next = edgeDict[here].pop(0)
        edgeDict[next].remove(here)
        road.append(next)
        if len(edgeDict[next]) == 0:
            del edgeDict[next]

    if next not in edgeDict:
        endpoint.remove(next)

    roads.append(road)


import matplotlib.pyplot as plt

for road in roads:
    lons, lats = zip(*road)
    plt.plot(lons, lats)

plt.grid()
plt.axis('equal')
plt.show()