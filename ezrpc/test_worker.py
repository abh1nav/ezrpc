#!/usr/bin/env python
# encoding: utf-8

import sys

import registry, server_worker

r = registry.Registry()

@r.method
def add(a, b):
    return a + b

w = server_worker.ServerWorker(sys.argv[1], r, "tcp://127.0.0.1:5000")
w.run()