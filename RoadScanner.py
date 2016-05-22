#!/usr/bin/env python
# coding: utf-8

import webbrowser
import matplotlib.pyplot as plt
import time
from collections import deque

from projection import project
from directions import *


plt.ion()

def location(endNode):
    f = 0.00001
    return (endNode[0] * f, endNode[1] * f)    


def run():
    start = (-3128042,-5220888)
    radius = 1

    fig = plt.figure()

    REQUEST_LIMIT = 25

    requests = 0

    # dirs = [n * 360.0/angleSteps for n in xrange(8)]

    nodeSet = set()
    seeds = deque()

    seeds.append(start)

    while (seeds):
        origin = location(seeds.popleft())
        print origin
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
                nodeSet.add(node)
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