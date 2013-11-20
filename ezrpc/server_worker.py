#!/usr/bin/env python
# encoding: utf-8

import json

import zmq

class ServerWorker(object):

    worker_id = None
    server_addr = None
    interrupted = False

    ctx = None
    socket = None
    poller = None
    connected = False

    registry = None

    def __init__(self, worker_id, registry, server_addr):
        """
        Initialize ServerWorker.
        Params:
            worker_id: String worker ID
            registry: A registry of RPC methods
            server_addr: Server address to connect to (tcp://127.0.0.1:5000)
        """
        self.worker_id = worker_id
        self.registry = registry
        self.server_addr = server_addr


    def _connect(self):
        """ Build up the socket & connect to the server. """
        self._disconnect()
        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.REP)
        self.poller = zmq.Poller()

        self.socket.connect(self.server_addr)
        self.poller.register(self.socket, zmq.POLLIN)

        self.connected = True
        print '[Worker %s] Connected to server' % self.worker_id


    def _disconnect(self):
        """ Disconnect any existing sockets, terminate contexts. """
        if self.socket:
            self.poller.unregister(self.socket)
            self.socket.close()
            print '[Worker %s] Disconnecting from server' % self.worker_id

        if self.ctx:
            self.ctx.term()


    def run(self):
        """ Wait for messages and do work. """
        self._connect()
        while not self.interrupted:
            self.poller.poll()
            try:
                req = json.loads(self.socket.recv(zmq.NOBLOCK))
                print 'Invoking method "%s"' % req['method']
                res = self.registry[req['method']](*req['args'])

                self.socket.send(str(res))
            except zmq.ZMQError:
                self._disconnect()
                self._connect()


    def invoke(self, method_name, *args):
        """ Invoke an RPC method. """
        self.registry(method_name, args)


    def interrupt(self):
        self.interrupted = True