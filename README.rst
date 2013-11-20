ezrpc
=====

Easy to use ZeroMQ based RPC library.

.. image:: https://pypip.in/v/ezrpc/badge.png
		:target: https://pypi.python.org/pypi/ezrpc

.. image:: https://pypip.in/d/ezrpc/badge.png
		:target: https://pypi.python.org/pypi/ezrpc

Install
=======

.. code-block:: text

	pip install ezrpc


Quickstart
==========

Step 1
------
Create a Server

.. code-block:: python

	# server.py
	from ezrpc import Server

	# By default, the server binds to all available interfaces
	s = Server(server_port=5000, client_port=5001)
	s.start()

Run this with:

.. code-block:: python

	python server.py


Step 2
------
Create a Worker

.. code-block:: python

	# worker.py
	from ezrpc import Registry, ServerWorker
	registry = Registry()

	@registry.method
	def add(a, b):
		return a + b

	@registry.method
	def multiply(a, b):
		return a * b

	# Point the worker to the Server's IP
	w = ServerWorker(sys.argv[1], registry, "tcp://127.0.0.1:5000")
	w.run()

Run as many workers as your server can handle:

.. code-block:: python

	python worker.py worker1
	python worker.py worker2
	python worker.py worker3

Workers are elastic, i.e. you can start and stop them at will and clients will continue to be served.

Step 3
------
Create a Client

.. code-block:: python

	# client.py
	from ezrpc import Client

	# Point the client to the Server's IP
	# timeout (millis) is optional, default is 5 seconds
	c = Client('tcp://127.0.0.1:5001', timeout=1000)

	for i in range(1,11):
		res = c.ask('add', i, 1)
		print 'Response: %s' % res

	c._disconnect()

Run the client

.. code-block:: python

	python client.py

