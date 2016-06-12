#!/usr/bin/env python
# coding: utf-8

# Dictionary of edges, indexed in both directions by node number.
edge = {}

with open('nodes.txt') as nodesfile:
    nodes = [(map(int, l.split(';'))) for l in nodesfile]
    nodesdict = {node[0] : (node[1], node[2]) for node in nodes}

# Ingest the data and build teh dictionary
with open("edges.txt") as efile:
    for line in efile:
        src, dst = line.strip().split(';')
        src = int(src)
        dst = int(dst)

        for key, val in [(src, dst), (dst, src)] :
            if key in edge:
                edge[key].append(val)
            else:
                edge[key] = ([val])
print "edge dictionary has entries:", len(edge)

# Identify endpoint nodes: order other than 2
#end_ct = 0
print "Endpoint Nodes"
endpoint = []
for src, dst in edge.iteritems():
    if len(dst) != 2:
        #print len(dst), src, dst
        endpoint.append(src)
        #end_ct += len(dst)
#print end_ct, "road ends"

atlas = []    # List of roads, each a list of nodes

# Build roads between the identified endpoints
# Pick the first endpoint in the remaining list.
# Move to the first-listed adjacent node.
# Keep going until we hit another node on the endpoint list.
while len(endpoint) > 0:
    here = endpoint[0]
#   print "Road starting at", here, edge[here]

    # Pick a first step and consume the edge
    next = edge[here].pop(0)
    edge[next].remove(here)
    road = [here, next]

    # If that's the last connection to the node, remove that node from the endpoints list.
    if len(edge[here]) == 0:
        del endpoint[0]
        del edge[here]
    # Special case for a one-segment road; endpoint entry of "next" is removed after the loop
    if len(edge[next]) == 0:
        del edge[next]

    # Consume edges until we reach another endpoint.
    debug = False
    while next not in endpoint:
        here = next
        next = edge[here].pop(0)
        edge[next].remove(here)
        road.append(next)
        if len(edge[next]) == 0:
            del edge[next]
#           print "removing node", next

    if next not in edge:
        endpoint.remove(next)
#       print "removing endpoint", next

    #print "\nRoad from", road[0], "to", road[-1], ':\n\t', road
    atlas.append(road)

print "\n", len(atlas), "roads built"
# print "edge dictionary still has entries:", len(edge)


import matplotlib.pyplot as plt

for road in atlas:
    path = [nodesdict[i] for i in road]
    lons, lats = zip(*path)
    plt.plot(lons, lats)

plt.grid()
plt.axis('equal')
plt.show()