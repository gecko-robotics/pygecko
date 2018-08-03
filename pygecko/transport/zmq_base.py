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
# from zmq.devices import ProcessProxy
import time
import socket as Socket
from pygecko.transport.protocols import Pickle

class ZMQError(Exception):
    pass


class Base(object):
    """
    Base class for other derived pub/sub/service classes
    """
    # ctx = zmq.Context()
    socket = None
    pack = None

    def __init__(self, kind=None):
        self.ctx = zmq.Context()
        self.pickle = Pickle()
        if kind:
            self.socket = self.ctx.socket(kind)
        else:
            self.socket = None

    def __del__(self):
        self.close()
        # self.ctx.term()
        # self.socket.close()
        # print('[<] shutting down {}'.format(type(self).__name__))

    def close(self):
        self.socket.close()
        self.ctx.term()
        print('[<] shutting down {}'.format(type(self).__name__))

    def bind(self, addr, hwm=None, queue_size=10):
        """
        Binds a socket to an addr. Only one socket can bind.
        Usually pub binds and sub connects, but not always!

        in:
          addr as tcp or uds
          hwm (high water mark) a int that limits buffer length
          queue_size is the same as hwm
        out: none
        """
        print(type(self).__name__, 'bind to {}'.format(addr))
        self.socket.bind(addr)
        if hwm:
            self.socket.set_hwm(hwm)
        elif queue_size:
            self.socket.set_hwm(queue_size)

    def connect(self, addr, hwm=None, queue_size=10):
        """
        Connects a socket to an addr. Many different sockets can connect.
        Usually pub binds and sub connects, but not always!

        in: addr as tcp or uds, hwm (high water mark) a int that limits buffer length
        out: none
        """
        print(type(self).__name__, 'connect to {}'.format(addr))
        self.socket.connect(addr)
        if hwm:
            self.socket.set_hwm(hwm)
        elif queue_size:
            self.socket.set_hwm(queue_size)
