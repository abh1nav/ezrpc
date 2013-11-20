#!/usr/bin/env python
# encoding: utf-8

import os
import sys

version = "0.1.0"

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist register upload")
    sys.exit(1)

# These are required because sometimes PyPI refuses to bundle certain files
try:
    long_desc = open('README').read()
except:
    long_desc = ""

try:
    license = open('LICENSE.txt').read()
except:
    license = "Apache 2.0 License"

setup(
    name='ezrpc',
    version=version,
    description='Easy to use ZeroMQ based RPC library',
    long_description=long_desc,
    author='Abhinav Ajgaonkar',
    author_email='abhinav316@gmail.com',
    packages=['ezrpc'],
    url='http://github.com/abh1nav/ezrpc/',
    license=license,
    install_requires=[
        "pyzmq==14.0.0"
    ]
)