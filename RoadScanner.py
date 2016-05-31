#!/usr/bin/env python
# coding: utf-8

import time
import os
from collections import deque

#import matplotlib.pyplot as plt

from projection import project
from directions import *


class PersistentSet(object):
    def __init__(self, fname):
        self._fname = fname
        self._items = {}

        if (not os.path.exists(self._fname)):
            with open(self._fname, 'w'):
                pass
        else:
            with open(self._fname) as itemsfile:
                for line in itemsfile:
                    self._deserializeItem(line)

    def _deserializeItem(self, string):
        raise Exception("not implemented")

    def __getitem__(self, key):
        return self._items[key]


class NodeSet(PersistentSet):
    def __init__(self, fname):
        super(NodeSet, self).__init__(fname)
        self._lastIndex = len(self._items)

    def _deserializeItem(self, string):
        index, lat, lon = map(int, string.strip().split(';'))
        node = (lat, lon)        
        self._items[node] = index

    def addNode(self, node):
        if node in self._items.values():
            return -1
        self._lastIndex += 1
        index = self._lastIndex        
        self._items[node] = index
        with open(self._fname, 'a') as nodesfile:
            nodesfile.write("{};{};{}\n".format(index, node[0], node[1]))
        return index

    def contains(self, node):
        return node in self._items

    def latlons(self):
        return zip(*list(self._items))


class EdgeSet(PersistentSet):
    def __init__(self, fname):
        super(EdgeSet, self).__init__(fname)

    def _deserializeItem(self, string):
        return tuple(map(int, string.strip().split(';')))

    def addEdge(self, edge):
        if edge in self._items:
            return
        with open(self._fname, 'a') as edgesfile:
            edgesfile.write("{};{}\n".format(*edge))


    def contains(self, edge):
        pass

    def latlonpairs(self):
        return [[]]


class Seeds(object):
    def __init__(self, fname):
        self._fname = fname
        self._seeds = deque()

        if (not os.path.exists(self._fname)):
            with open(self._fname, 'w'):
                pass
        else:
            with open(self._fname) as nodesfile:
                self._seeds = deque([tuple(map(int, l.split(';'))) for l in nodesfile if l])

    def push(self, seed):
        if seed not in self._seeds:
            self._seeds.append(seed)
            with open(self._fname, 'w') as out:
                out.writelines(["{};{}\n".format(*seed) for seed in self._seeds])

    def pop(self):
        return self._seeds.popleft()

    def purge(self, node):
        if node in self._seeds:
            self._seeds.remove(node)

    def latlons(self):
        return zip(*self._seeds) 


def run():
    radius = 10

    # plt.ion()
    # fig = plt.figure()

    nodes = NodeSet('nodes.txt')
    edges = EdgeSet('edges.txt')
    seeds = Seeds('seeds.txt')

    start = (-3120000,-5220800)
    seeds.push(start)

    while (seeds):

        seed = seeds.pop()
        origin = [v * 1e-5 for v in seed]

        for direction in xrange(0, 360, 90):      

            destination = project(origin, direction, radius)
            
            road = getDirections(origin, destination)

            if not road or not len(road) > 4:
                continue

            road = road[1:-1] # endpoints can be interpolated by directions api - this is not desireable

            endNode = road[-1]

            if not nodes.contains(endNode):
                seeds.push(endNode)
                # fig.gca().plot(endNode[1], endNode[0], 'o')

            for n in xrange(len(road)-1):
                firstnode = road[n]
                nextnode = road[n+1]

                #####################################
                ## nodes are not being added properly by "nodes.addNode(node)"

                firstindex = nodes.addNode(firstnode)
                nextindex = nodes.addNode(nextnode)

                if firstindex < 0:
                    continue

                seeds.purge(firstnode)

                edge = tuple(sorted([firstindex, nextindex]))
                edges.addEdge(edge)


            # fig.clf()
            # fig.gca().axis('equal')

            # lats, lons = nodes.latlons()
            # fig.gca().scatter(lons, lats, s=4, linewidths=0, color='k', alpha=0.3)

            ##### here the segments should be plotted
            ##### looks like it would be very slow, so perhaps
            ##### use idea from here: http://stackoverflow.com/a/21356103/401828
            
            # slat, slon = seeds.latlons()
            # fig.gca().scatter(slon, slat, color='r', s=30, linewidths=0)

            # fig.canvas.draw()

            # time.sleep(0.5)

run()


plt.show(block=True)