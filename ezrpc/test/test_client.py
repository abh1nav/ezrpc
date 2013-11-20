#!/usr/bin/env python
# encoding: utf-8

import time

from ezrpc import Client

c = Client('tcp://127.0.0.1:5001', timeout=1000)

for i in range(1,11):
    res = c.ask('add', i, 1)
    print 'Response: %s' % res
    time.sleep(1)

c._disconnect()