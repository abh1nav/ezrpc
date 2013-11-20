#!/usr/bin/env python
# encoding: utf-8

import sys

from ezrpc import Registry, ServerWorker

r = Registry()

@r.method
def add(a, b):
    return a + b

w = ServerWorker(sys.argv[1], r, "tcp://127.0.0.1:5000")
w.run()