'''
The MIT License (MIT)
Copyright (c) 2013 Dave P.
'''

import os
import signal
import sys
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer


class SimpleEcho(WebSocket):

    _fname = 'roads.txt'

    def handleMessage(self):
        print "message"

        if not os.path.exists(self._fname):
            print "gonna save the file"
            with open(self._fname, 'w'):
                pass  
                
        with open(self._fname, 'a') as out:
            out.write(self.data)
            out.write("\n")

    def handleClose(self):
        print "close"

    def handleOpen(self):
        print "open"



if __name__ == "__main__":

    server = SimpleWebSocketServer("localhost", 8000, SimpleEcho)

    print "serving at ws://localhost:8000"

    def close_sig_handler(signal, frame):
        server.close()
        sys.exit()

    signal.signal(signal.SIGINT, close_sig_handler)

    server.serveforever()
