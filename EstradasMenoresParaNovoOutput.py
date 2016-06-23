#!/usr/bin/env python
# coding: utf-8

import time
import json
import glob
import re


import networkx as nx
from networkx.readwrite import json_graph




lastfile = sorted(glob.glob('output/*.json'))[-1]
with open(lastfile) as jsonfile:
    jsondict = json.load(jsonfile)

nodes = [tuple(node['id']) for node in jsondict['nodes']]
edges = [(nodes[edge['source']], nodes[edge['target']]) for edge in jsondict['links']]

graph = nx.Graph()
graph.add_edges_from(edges)

print graph.number_of_nodes()





kmls = glob.glob('../../../01 Helton Moraes/Experiments/KmlHacker/Estradas*.kml')

for kml in kmls:
    with open(kml) as kmlin:
        source = kmlin.read();
        for linestring in re.findall("<LineString>.*?</LineString>", source, re.DOTALL):
            coordinates = re.search("<coordinates>(.*?)</coordinates>", linestring, re.DOTALL).group(1).strip()
            coordlist = re.split('\s+', coordinates)
            coords = []
            for fields in coordlist:
                lonstring, latstring = fields.split(',')[:2]
                lon, lat = map(lambda x:int(float(x)*1e5), [lonstring, latstring])
                coord = (lon, lat)
                if not coords or coord != coords[-1]:
                    coords.append((lon, lat))
            graph.add_path(coords)

print graph.number_of_nodes()

timestamp = int(time.time()*1e3)
fname = "output/{} roadgraph.json".format(timestamp)
with open(fname, 'w') as graphfile:
    json.dump(json_graph.node_link_data(graph), graphfile)
