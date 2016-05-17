#!/usr/bin/env python
# coding: utf-8

import json
import urllib
import numpy
import matplotlib.pyplot as plt
import math
import time

def ll2str(ll):
    return "%f,%f" % ll

def project(point, angle, distance):
    rads = math.radians(angle)
    nx = point[0] + distance * math.sin(rads)
    ny = point[1] + distance * math.cos(rads)
    return (nx, ny)

def polydecode(point_str):
    '''Decodes a polyline that has been encoded using Google's algorithm
    http://code.google.com/apis/maps/documentation/polylinealgorithm.html

    This is a generic method that returns a list of (latitude, longitude)
    tuples.

    :param point_str: Encoded polyline string.
    :type point_str: string
    :returns: List of 2-tuples where each tuple is (latitude, longitude)
    :rtype: list

    '''

    # sone coordinate offset is represented by 4 to 5 binary chunks
    coord_chunks = [[]]
    for char in point_str:

        # convert each character to decimal from ascii
        value = ord(char) - 63

        # values that have a chunk following have an extra 1 on the left
        split_after = not (value & 0x20)
        value &= 0x1F

        coord_chunks[-1].append(value)

        if split_after:
                coord_chunks.append([])

    del coord_chunks[-1]

    coords = []

    for coord_chunk in coord_chunks:
        coord = 0

        for i, chunk in enumerate(coord_chunk):
            coord |= chunk << (i * 5)

        #there is a 1 on the right if the coord is negative
        if coord & 0x1:
            coord = ~coord #invert
        coord >>= 1
        coord /= 100000.0

        coords.append(coord)

    # convert the 1 dimensional list to a 2 dimensional list and offsets to
    # actual values
    points = []
    prev_x = 0
    prev_y = 0
    for i in xrange(0, len(coords) - 1, 2):
        if coords[i] == 0 and coords[i + 1] == 0:
            continue

        prev_x += coords[i + 1]
        prev_y += coords[i]
        # a round to 6 digits ensures that the floats are the same as when
        # they were encoded
        points.append((round(prev_x, 6), round(prev_y, 6)))

    return points

geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?latlng={[lat]},{[lon]}&sensor=false'
directions_url = 'http://maps.googleapis.com/maps/api/directions/json?sensor=false&origin={}&destination={}'

origin = (-30.2664935,-51.8364501)

for dist in [0.1, 0.05, 0.01, 0.005, 0.001]:
    paths = []
    plt.figure()
    for angle in range(0, 360, 45):
        np = project(origin, angle, dist)
        plt.scatter(np[1], np[0])
        pars = (ll2str(origin), ll2str(np))
        request_url = directions_url.format(*pars)
        result_string = urllib.urlopen(request_url).read();
        result = json.loads(result_string)
        # print result; exit()
        if result['status'] == "OK":
            rota = result['routes'][0]
            for leg in rota['legs']:
                for step in leg['steps']:
                    encodedpoints = step['polyline']['points']
                    print encodedpoints
                    paths.append(numpy.array(polydecode(encodedpoints)))
        else:
            "status não ok!"
        time.sleep(1)


    for path in paths:
        plt.plot(path[:,0], path[:,1], 'o-', c='b', ms=3, mew=0, alpha=0.3)
        plt.axis('equal')

plt.show()
