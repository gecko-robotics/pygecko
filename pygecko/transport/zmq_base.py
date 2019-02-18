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
# import time
# import socket as Socket
from pygecko.transport.protocols import Pickle
from pygecko.transport.protocols import MsgPack,MsgPackCustom

class ZMQError(Exception):
    pass


class Base(object):
    """
    Base class for other derived pub/sub/service classes
    """
    # ctx = zmq.Context()
    # socket = None
    # pack = None
    # topics = None

    def __init__(self, kind=None, serialize=MsgPack):  # FIXME: kind is not used???
        self.topics = None
        self.pack = None  # ???
        self.ctx = zmq.Context()
        self.pickle = serialize()  # use pack or serialize??
        if kind:
            self.socket = self.ctx.socket(kind)
        else:
            self.socket = None

    def __del__(self):
        """Calls close()"""
        self.close()
        # self.ctx.term()
        # self.socket.close()
        # print('[<] shutting down {}'.format(type(self).__name__))

    def close(self):
        """Closes socket and terminates context"""
        self.socket.close()
        self.ctx.term()
        # print('[<] shutting down {}'.format(type(self).__name__))

    def bind(self, addr, hwm=None, queue_size=10, random=False):
        """
        Binds a socket to an addr. Only one socket can bind.
        Usually pub binds and sub connects, but not always!

        args:
          addr as tcp or uds
          hwm (high water mark) a int that limits buffer length
          queue_size is the same as hwm
          random: select a random port to bind to
        return: port number
        """
        # print(type(self).__name__, 'bind to {}'.format(addr))
        if random:
            # https://pyzmq.readthedocs.io/en/latest/api/zmq.html#zmq.Socket.bind_to_random_port
            port = self.socket.bind_to_random_port(addr)  # tcp://* ???
        else:
            port = int(addr.split(':')[2])  # tcp://ip:port
            self.socket.bind(addr)

        if hwm:
            self.socket.set_hwm(hwm)
        elif queue_size:
            self.socket.set_hwm(queue_size)

        return port

    def connect(self, addr, hwm=None, queue_size=10):
        """
        Connects a socket to an addr. Many different sockets can connect.
        Usually pub binds and sub connects, but not always!

        args:
            addr as tcp or uds
            hwm (high water mark) a int that limits buffer length
            queue_size is the same as hwm
        return: none
        """
        # print(type(self).__name__, 'connect to {}'.format(addr))
        self.socket.connect(addr)
        if hwm:
            self.socket.set_hwm(hwm)
        elif queue_size:
            self.socket.set_hwm(queue_size)
