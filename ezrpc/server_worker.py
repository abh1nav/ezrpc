#!/usr/bin/env python
# encoding: utf-8


class ServerWorker(object):

    server_addr = None
    ctx = None
    socket = None

    registry = None

    def __init__(self, registry):
        self.registry = registry


    def invoke(self, method_name, *args):
        self.registry(method_name, args)