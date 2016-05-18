#!/usr/bin/env python
# coding: utf-8

import urllib
import json

from polylineEncoding import decodePolyline

directions_template = 'http://maps.googleapis.com/maps/api/directions/json?sensor=false&origin={},{}&destination={},{}'

def getDirections(origin, destination):
    url = directions_template.format(origin[0], origin[1], destination[0], destination[1])
    response = urllib.urlopen(url).read();
    directions = json.loads(response)
    # print directions; exit()
    road = []
    if directions['status'] == "OK":
        rota = directions['routes'][0]
        for leg in rota['legs']:
            for step in leg['steps']:
                encodedpoints = step['polyline']['points']
                points = decodePolyline(encodedpoints)
                road.extend(points)
    return road

