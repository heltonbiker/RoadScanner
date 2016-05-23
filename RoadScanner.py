#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import time
import os
from collections import deque

from projection import project
from directions import *


# TODO:
# Load seeds from file at start, and serialize them back periodically

class NodeSet(object):
    def __init__(self, fname):

        self._fname = fname
        self._nodes = set()

        if (not os.path.exists(nodesfname)):
            with open(nodesfname, 'w'):
                pass
        else:
            try:
                with open(self._fname) as nodesfile:
                    self._nodes.update(map(int, l.split(';')) for l in nodesfile)

    def addNode(self, node):
        self._nodes.add(node)
        with open(self._fname, 'a') as nodesfile:
            nodesfile.writeline("{};{}".format(node))


def location(endNode):
    f = 0.00001
    return (endNode[0] * f, endNode[1] * f)    


def run():
    radius = 1

    plt.ion()
    fig = plt.figure()

    REQUEST_LIMIT = 25

    requests = 0

    nodeSet = NodeSet('nodes.txt')
    start = (-3128042,-5220888)
    nodeSet.addNode(start)


    seeds = deque()

    seeds.append(start)

    while (seeds):

        origin = location(seeds.popleft())

        for direction in xrange(0, 360, 30):     
         
            destination = project(origin, direction, radius)
            
            road = getDirections(origin, destination)

            if not road:
                continue

            endNode = road[-1]

            if not endNode in nodeSet:
                seeds.append(endNode)
                fig.gca().plot(endNode[1], endNode[0], 'o')

            for node in road[:-1]:
                nodeSet.addNode(node)
                if node in seeds:
                    seeds.remove(node)

            fig.clf()
            fig.gca().axis('equal')

            lats, lons = zip(*list(nodeSet))
            fig.gca().scatter(lons, lats, s=4, linewidths=0, color='k', alpha=0.3)
            
            slat, slon = zip(*seeds)
            fig.gca().scatter(slon, slat, color='r', s=30, linewidths=0)

            fig.canvas.draw()

            requests += 1
            # if requests > REQUEST_LIMIT:
            #     return

            time.sleep(0.3)

run()


plt.show(block=True)