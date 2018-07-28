##############################################
# The MIT License (MIT)
# Copyright (c) 2014 Kevin Walchko
# see LICENSE for full details
##############################################
#
# Kevin J. Walchko 13 Oct 2014
#
# see http://zeromq.org for more info
# http://zguide.zeromq.org/py:all

from __future__ import print_function
from __future__ import division
import zmq
import socket as Socket

def zmq_version():
    """
    What version of the zmq (C++) library is python tied to?
    """
    print('Using ZeroMQ version: {0!s}'.format((zmq.zmq_version())))


def zmqTCP(host, port):
    """
    Set the zmq address as TCP: tcp://host:port
    """
    if host == 'localhost':  # do I need to do this?
        host = Socket.gethostbyname(Socket.gethostname())
    return 'tcp://{}:{}'.format(host, port)


def zmqUDS(mnt_pt):
    """
    Set the zmq address as a Unix Domain Socket: ipc://file
    """
    return 'ipc://{}'.format(mnt_pt)
