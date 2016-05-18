#!/usr/bin/env python
# coding: utf-8

import webbrowser

from projection import project

def scanRoads(origin, radius):
    result = []

    angleSteps = 8
    step = 360.0/angleSteps
    dirs = [n * step for n in xrange(angleSteps)]
    for direction in dirs:
        newPoint = project(origin, direction, radius)
        result.append([origin, newPoint])

    print result
    return result




if __name__ == '__main__':
    origin = (-30.2664935,-51.8364501)
    radius = 10

    paths = scanRoads(origin, radius)

    import matplotlib.pyplot as plt
    for path in paths:
        lats, lons = zip(*path)
        plt.plot(lons, lats)

    plt.axis('equal')
    plt.grid()
    plt.show()
    exit()

    from createMap import createMap
    createMap(paths, "map.html")
    webbrowser.open("map.html")