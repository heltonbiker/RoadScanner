#!/usr/bin/env python
# coding: utf-8

import webbrowser

from projection import project
from directions import *

def getSegments(road):
    return [(road[n-1], road[n]) for n in xrange(1, len(road))]

def scanRoads(origin, radius):
    result = []

    angleSteps = 8
    step = 360.0/angleSteps
    dirs = [n * step for n in xrange(angleSteps)]
    for direction in dirs:
        destination = project(origin, direction, radius)
        road = getDirections(origin, destination)
        #segments = getSegments(road)

        result.append(road)

    return result




if __name__ == '__main__':
    origin = (-30.2664935,-51.8364501)
    radius = 10

    roads = scanRoads(origin, radius)

    from createMap import createMap
    createMap(roads, "map.html")
    webbrowser.open("map.html")

    # import matplotlib.pyplot as plt
    # for road in roads:
    #     lats, lons = zip(*road)
    #     #print lats, lons
    #     plt.plot(lons, lats, 'o-', ms=3, mew=0)

    # plt.grid()
    # plt.show()    