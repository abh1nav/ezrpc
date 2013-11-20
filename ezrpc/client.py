#!/usr/bin/env python
# encoding: utf-8

import json

import zmq

class Client(object):

    server_addr = None

    ctx = None
    socket = None
    poller = None
    connected = False
    timeout = None

    def __init__(self, server_addr, timeout=5000):
        self.server_addr = server_addr
        self.timeout = timeout


    def _connect(self):
        """ Build up the socket & connect to the server. """
        self._disconnect()
        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.REQ)
        self.poller = zmq.Poller()

        self.socket.connect(self.server_addr)
        self.poller.register(self.socket, zmq.POLLIN)

        self.connected = True
        print '[Client] Connected to RPC server'


    def _disconnect(self):
        """ Disconnect any existing sockets, terminate contexts. """
        if self.socket:
            try:
                self.poller.unregister(self.socket)
            finally:
                self.poller = None

            try:
                self.socket.close()
            finally:
                self.socket = None
            print '[Client] Disconnecting from RPC server'

        if self.ctx:
            self.ctx.term()


    def ask(self, method, *args):
        """ Send a message to the RPC server. """
        if not self.connected:
            self._connect()

        msg = '{"method":"%s","args":%s}' % (method, json.dumps(args))
        self.socket.send(msg)
        try:
            self.poller.poll(timeout=self.timeout)
            resp = self.socket.recv(zmq.NOBLOCK)
            return resp
        except zmq.ZMQError:
            self._disconnect()
            self._connect()