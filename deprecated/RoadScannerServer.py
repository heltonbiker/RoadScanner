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

    def handleOpen(self):
        print "open"
        print dir(self)

    def handleConnected(self):
        with open(self._fname) as roadsfile:
            lines = roadsfile.readlines()
            for line in lines:
                numbers = map(float, re.split('[\s,]+', line.strip()))
                a = array('d', numbers)       
                self.sendMessage(a.tostring())

        # print (self.address, 'connected')
        # for client in clients:
        #     client.sendMessage(self.address[0] + u' - connected')
        # clients.append(self)        

    def handleMessage(self):
        # print "message"
        # print dir(self)
        # print self.client
        # print self.data

        if not os.path.exists(self._fname):
            print "gonna save the file"
            with open(self._fname, 'w'):
                pass  
                
        with open(self._fname, 'a') as out:
            print "writing road to file"
            out.write(self.data)
            out.write("\n")

      # for client in clients:
      #    if client != self:
      #       client.sendMessage(self.address[0] + u' - ' + self.data)            

    def handleClose(self):
        print "close"


if __name__ == "__main__":

    # with open('roads.txt') as roadsfile:

    #     content = roadsfile.read()
    #     numbers = map(float, re.split('[\s,].?', content.strip()))
    #     a = array('d', numbers)
    #     print a.tostring()

    #     exit()


    server = SimpleWebSocketServer("localhost", 8000, RoadsSocket)

    print "serving at ws://localhost:8000"

    def close_sig_handler(signal, frame):
        server.close()
        sys.exit()

    signal.signal(signal.SIGINT, close_sig_handler)

    server.serveforever()
