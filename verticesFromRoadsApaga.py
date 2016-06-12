#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import networkx

nodes = []
nodeindices = []

edges = []
edgeindices = []

with open('roads.txt') as roadsFile:
    lines = roadsFile.readlines()
    total = len(lines)
    for n, line in enumerate(lines):
        print "processing line {} of {}".format(n+1, total)
        road = [tuple(map(lambda x:int(float(x)*1e5), coord.split(','))) for coord in line.strip().split(' ')]
        for n in xrange(len(road)-1):
            firstnode = road[n]
            secondnode = road[n+1]

            alreadyfirst = firstnode in nodes
            alreadysecond = secondnode in nodes

            if alreadyfirst and alreadysecond:
                continue

            if not alreadyfirst and not alreadysecond:
                nodes.append(firstnode)
                nodes.append(secondnode)
                edge = (len(nodes)-1, len(nodes))
                edges.append(edge)


            if alreadyfirst and not alreadysecond:
                firstindex = nodes.index(firstnode) + 1
                nodes.append(secondnode)
                secondindex = len(nodes)

                edge = tuple(sorted([firstindex, secondindex]))
                edges.append(edge)

            if alreadysecond and not alreadyfirst:
                secondindex = nodes.index(secondnode) + 1
                nodes.append(firstnode)
                firstindex = len(nodes)

                edge = tuple(sorted([firstindex, secondindex]))
                edges.append(edge)

with open('nodes.txt', 'w') as nodesfile:
    nodesfile.write('\n'.join(['{};{};{}'.format(n+1, e[0], e[1]) for n, e in enumerate(nodes)]))

with open('edges.txt', 'w') as edgesfile:
    edgesfile.write('\n'.join(['{};{}'.format(*e) for e in edges]))

for edge in edges:
    firstindex, secondindex = edge
    firstpoint = nodes[firstindex-1]
    secondpoint = nodes[secondindex-1]
    lats, lons = zip(firstpoint, secondpoint)
    plt.plot(lats, lons, 'b')

plt.show()
