'''
The MIT License (MIT)
Copyright (c) 2013 Dave P.
'''

import os
import signal
import sys
from array import array
import codecs
import re
import json
import time
import glob
import itertools
import webbrowser

import networkx as nx
from networkx.readwrite import json_graph

from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer

# handlers to override in WebSocket:
# handleMessage:   called when websocket frame is received;
# handleConnected: called when client connects to the server;
# handleClose:     called when server gets "close" from a client;
# sendMessage:     send frame to the client
#
#



class RoadsSocket(WebSocket):

    _clients = []
    _fname = 'roads.txt'

    graph = nx.Graph()

    def handleOpen(self):
        print "open"
        print dir(self)

    def handleConnected(self):
        # with open(self._fname) as roadsfile:
        #     lines = roadsfile.readlines()
        #     for line in lines:
        #         numbers = map(float, re.split('[\s,]+', line.strip()))
        #         road = [tuple(map(lambda x:int(float(x)*1e5), coord.split(','))) for coord in line.strip().split(' ')]
        #         a = array('d', numbers)       
        #         self.sendMessage(a.tostring())

        lastfile = sorted(glob.glob('output/*.json'))[-1]
        with open(lastfile) as jsonfile:
            jsondict = json.load(jsonfile)

        nodes = [tuple(node['id']) for node in jsondict['nodes']]
        edges = [(nodes[edge['source']], nodes[edge['target']]) for edge in jsondict['links']]

        self.graph = nx.Graph()
        self.graph.add_edges_from(edges)

        self.sendRoads()

        #print (self.address, 'connected')
        # for client in clients:
        #     client.sendMessage(self.address[0] + u' - connected')
        # clients.append(self)

    def sendRoads(self):
        edgeDict = {}

        for edge in self.graph.edges():
            src, dst = edge
            for key, val in [(src, dst), (dst, src)] :
                if key in edgeDict:
                    edgeDict[key].append(val)
                else:
                    edgeDict[key] = ([val])


        # Identify endpoint nodes: order other than 2
        endpoint = []
        for src, dst in edgeDict.iteritems():
            if len(dst) != 2:
                endpoint.append(src)

        roads = []    # List of roads, each a list of nodes

        # Build roads between the identified endpoints
        # Pick the first endpoint in the remaining list.
        # Move to the first-listed adjacent node.
        # Keep going until we hit another node on the endpoint list.
        while len(endpoint) > 0:
            here = endpoint[0]

            # Pick a first step and consume the edge
            next = edgeDict[here].pop(0)
            edgeDict[next].remove(here)
            road = [here, next]

            # If that's the last connection to the node, remove that node from the endpoints list.
            if len(edgeDict[here]) == 0:
                del endpoint[0]
                del edgeDict[here]

            # Special case for a one-segment road; endpoint entry of "next" is removed after the loop
            if len(edgeDict[next]) == 0:
                del edgeDict[next]

            # Consume edges until we reach another endpoint.
            while next not in endpoint:
                here = next
                next = edgeDict[here].pop(0)
                edgeDict[next].remove(here)
                road.append(next)
                if len(edgeDict[next]) == 0:
                    del edgeDict[next]

            if next not in edgeDict:
                endpoint.remove(next)

            roads.append(road)

        for road in roads:
            chained = list(itertools.chain(*road))
            a = array('i', chained)       
            self.sendMessage(a.tostring())            


    def handleMessage(self):
        # print "message"
        # print dir(self)
        # print self.client

        try:
            road = [tuple(map(lambda x:int(x), pair.split(','))) for pair in self.data.strip().split(' ')]
            for pair in zip(road[:-1], road[1:]):
                if pair[0] == pair[1]:
                    print pair
            self.graph.add_path(road)
            #print self.graph.number_of_edges()
            #print json.dumps({'nodes': self.graph.nodes(), 'edges': self.graph.edges()})
            timestamp = int(time.time()*1e3)
            fname = "output/{} roadgraph.json".format(timestamp)
            with open(fname, 'w') as graphfile:
                json.dump(json_graph.node_link_data(self.graph), graphfile)
            print "saved file with {} nodes".format(self.graph.number_of_nodes())
        except Exception as e:
            print e

    def handleClose(self):
        print "close"


if __name__ == "__main__":

    server = SimpleWebSocketServer("localhost", 8000, RoadsSocket)

    print "serving at ws://localhost:8000"

    def close_sig_handler(signal, frame):
        server.close()
        sys.exit()

    signal.signal(signal.SIGINT, close_sig_handler)

    # webbrowser.open_new('RoadScanner.html')

    server.serveforever()
