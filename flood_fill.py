#!/usr/bin/env python
# coding: utf-8

import json
import urllib
import numpy
import matplotlib.pyplot as plt
import math
import time

from polylineEncoding import *

def stringifyPosition(ll):
    return "%f,%f" % ll

def project(point, angle, distance):
    rads = math.radians(angle)
    nx = point[0] + distance * math.sin(rads)
    ny = point[1] + distance * math.cos(rads)
    return (nx, ny)


geocode_url = 'http://maps.googleapis.com/maps/api/geocode/json?latlng={[lat]},{[lon]}&sensor=false'
directions_url = 'http://maps.googleapis.com/maps/api/directions/json?sensor=false&origin={},{}&destination={},{}'

origin = (-30.2664935,-51.8364501)

dist = 0.005

paths = []
plt.figure()
for angle in range(0, 360, 45):
    np = project(origin, angle, dist)
    plt.scatter(np[1], np[0])
    request_url = directions_url.format(*sum((origin, np),()))
    result_string = urllib.urlopen(request_url).read();
    result = json.loads(result_string)
    # print result; exit()
    if result['status'] == "OK":
        rota = result['routes'][0]
        for leg in rota['legs']:
            for step in leg['steps']:
                encodedpoints = step['polyline']['points']
                print encodedpoints
                paths.append(numpy.array(decodePolyline(encodedpoints)))
    else:
        "status não ok!"
    time.sleep(1)

for path in paths:
    plt.plot(path[:,0], path[:,1], 'o-', c='b', ms=3, mew=0, alpha=0.3)

plt.axis('equal')
plt.show()
