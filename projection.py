#!/usr/bin/env python
# coding: utf-8

import math

def project(origin, direction, radius):
    R = 6378.1

    brng = math.radians(direction)
    d = radius

    lat1 = math.radians(origin[0])
    lon1 = math.radians(origin[1])

    lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
         math.cos(lat1)*math.sin(d/R)*math.cos(brng))

    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
                 math.cos(d/R)-math.sin(lat1)*math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    return [lat2, lon2]