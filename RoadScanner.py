#!/usr/bin/env python
# coding: utf-8

import webbrowser

from projection import project
from directions import *

def scanRoads(origin, radius):
    result = []

    angleSteps = 8
    step = 360.0/angleSteps
    dirs = [n * step for n in xrange(angleSteps)]
    for direction in dirs:
        destination = project(origin, direction, radius)
        road = getDirections(origin, destination)
        result.append(road)

    return result




if __name__ == '__main__':
    origin = (-30.2664935,-51.8364501)
    radius = 10

    roads = scanRoads(origin, radius)

    import matplotlib.pyplot as plt
    for road in roads:
        lats, lons = zip(*road)
        plt.plot(lons, lats)

    plt.axis('equal')
    plt.grid()
    plt.show()
    exit()

    from createMap import createMap
    createMap(roads, "map.html")
    webbrowser.open("map.html")