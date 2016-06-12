#!/usr/bin/env python
# coding: utf-8

import time
import os
from collections import deque

#import matplotlib.pyplot as plt

from projection import project
from directions import *

from PersistentSets import *



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