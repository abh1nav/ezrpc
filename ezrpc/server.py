#!/usr/bin/env python
# encoding: utf-8

import time

import zmq

class Server(object):

    transport = None
    interface = None
    server_port = None
    client_port = None

    ctx = None
    frontend = None
    backend = None

    def __init__(self, transport="tcp", interface="*", server_port=5000, client_port=5001):
        """
        Initialize the server.
        Params:
            transport: The type of transport to use. Valid transports are: tcp, ipc, icp, udp
            interface: The address of the interface to bind to
            server_port: The port number to bind to - the server workers will connect here
            client_port: The port number to bind to - the clients will connect here
        """
        self.transport = transport
        self.interface = interface
        self.server_port = server_port
        self.client_port = client_port


    def start(self):
        """
        Start the server.
        Note: this is a blocking call.
        """
        while True:
            try:
                print "Starting ZRPC server"
                self.ctx = zmq.Context()

                self.backend = self.ctx.socket(zmq.XREQ)
                print "Listening for server workers on %s" % self._get_server_addr()
                self.backend.bind(self._get_server_addr())

                self.frontend = self.ctx.socket(zmq.XREP)
                print "Listening for clients on %s" % self._get_client_addr()
                self.frontend.bind(self._get_client_addr())

                zmq.device(zmq.QUEUE, self.frontend, self.backend)

            except Exception as e:
                print 'Exception in ZRPC server: %s' % str(e)
                print 'Stopping ZRPC server'
                self.frontend.close()
                self.backend.close()
                self.ctx.term()
                time.sleep(3)


    def _get_server_addr(self):
        return '%s://%s:%s' % (self.transport, self.interface, self.server_port)


    def _get_client_addr(self):
        return '%s://%s:%s' % (self.transport, self.interface, self.client_port)
