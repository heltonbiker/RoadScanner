#!/usr/bin/env python
# coding: utf-8

import json
import urllib
import numpy
import matplotlib.pyplot as plt

lats = numpy.linspace(-31, -30, 11)
lons = numpy.linspace(-52, -51, 11)

#for lat in lats:
    #for lon in lons:
        #plt.plot(

grid = numpy.transpose([numpy.tile(lats, lons.size), numpy.repeat(lons, lats.size)])

locs = []

for p in grid:
    url = 'http://maps.googleapis.com/maps/api/geocode/json?latlng={0},{1}&sensor=false'.format(*p)
    response = urllib.urlopen(url).read()
    data = json.loads(response)

    print response

    exit()
    
    for result in data['results']:
        loc = result['geometry']['location']
        
        lats = (p[0], loc['lat'])
        lons = (p[1], loc['lng'])
        
        plt.plot(lons, lats, 'o-')
        
        #locs.append((loc['lat'], loc['lng']))
        
#locs = numpy.array(locs)

#plt.scatter(locs[:,1], locs[:,0], s=5, color='cyan')

#plt.scatter(grid[:,1], grid[:,0], s=5, color='blue')

plt.axis('equal')

plt.show()
