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
from zmq.devices import ProcessProxy
import time
# import simplejson as json
import socket as Socket
# from .Messages import serialize, deserialize
import msgpack


class ZMQError(Exception):
    pass


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


class Core(object):
    """
    http://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/devices/forwarder.html
    """
    def __init__(self, inaddr=None, outaddr=None):
        core = ProcessProxy(zmq.SUB, zmq.PUB)
        self.core = core

        if inaddr is None:
            inaddr = zmqTCP('localhost', 9998)
        if outaddr is None:
            outaddr = zmqTCP('localhost', 9999)

        # inputs (sub)
        core.bind_in(inaddr)
        core.setsockopt_in(zmq.SUBSCRIBE, b'')

        # outputs (pub)
        core.bind_out(outaddr)
        core.start()

        print('Core ---------------------')
        # print("core:", core)
        print('  In[sub]: {}'.format(inaddr))
        print('  Out[pub]: {}'.format(outaddr))
        print('-'*30)

    def __del__(self):
        # self.input.close()
        # self.out.close()
        # self.ctx.term()
        self.core.join(1)
        print("Core exiting")

    def join(self, timeout=1):
        self.core.join(timeout)

class GeckoCore(Core):
    pass

class Base(object):
    """
    Base class for other derived pub/sub/service classes
    """
    # ctx = zmq.Context()
    socket = None
    pack = None

    def __init__(self):
        self.ctx = zmq.Context()

    def __del__(self):
        self.ctx.term()
        print('[<] shutting down {}'.format(type(self).__name__))

    def bind(self, addr):
        print(type(self).__name__, 'bind to {}'.format())
        self.socket.bind(addr)

    def connect(self, addr):
        print(type(self).__name__, 'connect to {}'.format(addr))
        self.socket.connect(addr)


class Pub(Base):
    """
    Simple publisher
    """
    def __init__(self, hwm=100, pack=None):
        Base.__init__(self)

        try:
            self.socket = self.ctx.socket(zmq.PUB)
            # self.socket.set_hwm(hwm)
            # self.socket.setsockopt(zmq.SNDHWM, 1)

        except Exception as e:
            error = '[-] Pub Error, {0!s}'.format((str(e)))
            raise ZMQError(error)

        if pack:
            self.pack = pack

    def __del__(self):
        self.socket.close()

    def pub(self, topic, msg):
        """
        It appears the send_json() doesn't work for pub/sub.
        in: topic, message
        out: none
        """
        # jmsg = serialize(msg)
        if self.pack:
            jmsg = msgpack.packb(msg, default=self.pack, use_bin_type=True, strict_types=True)
        else:
            jmsg = msgpack.packb(msg, use_bin_type=True, strict_types=True)
        # self.socket.send_multipart([topic.encode('ascii'), jmsg.encode('ascii')])
        done = True
        while done:
            done = self.socket.send_multipart([topic.encode('ascii'), jmsg])
            # done = self.socket.send(jmsg)
        # print('pub >>', topic.encode('ascii'))


class Sub(Base):
    """
    Simple subscriber
    """
    unpack = None

    def __init__(self, topics=None, hwm=100, unpack=None):
        Base.__init__(self)
        if type(topics) is list:
            pass
        else:
            raise Exception('topics must be a list')
            # topics = [topics]

        self.topics = topics
        try:
            self.socket = self.ctx.socket(zmq.SUB)
            # self.socket.set_hwm(hwm)  # set high water mark, so imagery doesn't buffer and slow things down

            # manage subscriptions
            # can also use: self.socket.subscribe(topic) or unsubscribe()
            if topics is None:
                print("[>] Receiving messages on ALL topics...")
                self.socket.setsockopt(zmq.SUBSCRIBE, b'')
            else:
                for t in topics:
                    print("[>] Subscribed to messages on topics: {} ...".format(t))
                    # self.socket.setsockopt(zmq.SUBSCRIBE, t.encode('ascii'))
                    self.socket.setsockopt(zmq.SUBSCRIBE, t.encode('ascii'))

        except Exception as e:
            error = '[-] Sub Error, {0!s}'.format((str(e)))
            # print error
            raise ZMQError(error)

        if unpack:
            self.unpack = unpack

    def __del__(self):
        if self.topics is None:
            self.socket.setsockopt(zmq.UNSUBSCRIBE, b'')
        else:
            for t in self.topics:
                self.socket.setsockopt(zmq.UNSUBSCRIBE, t.encode('ascii'))
        self.socket.close()

    def recv(self, flags=0):
        """
        flags=zmq.NOBLOCK to implement non-blocking
        """
        topic = None
        msg = None
        try:
            topic, jmsg = self.socket.recv_multipart(flags=flags)
            if self.unpack:
                msg = msgpack.unpackb(jmsg, ext_hook=self.unpack, raw=False)
            else:
                msg = msgpack.unpackb(jmsg, raw=False)
        except zmq.Again as e:
            # no message has arrived yet
            print(e)
            pass
        except Exception as e:
            # something else is wrong
            print(e)
            raise
        return topic, msg

    # def recv(self):
    #     # check to see if there is read, write, or erros
    #
    #     topic = None
    #     msg = None
    #
    #     zmq.zmq_poll([(self.socket, zmq.POLLIN,)], 10)
    #     socks = self.poller.poll(10)
    #     print('socks', socks)
    #     socks = dict(socks)
    #     topic, jmsg = self.socket.recv_multipart()
    #     print(topic)
    #
    #     print('socks:', socks)
    #
    #     cnt = 0
    #     if socks.get(self.socket) == zmq.POLLIN:
    #         print('pollin:')
    #         try:
    #             for i in range(10):
    #                 topic, jmsg = self.socket.recv_multipart()
    #                 msg = deserialize(jmsg)
    #                 cnt = i
    #         except:
    #             pass
    #
    #         print('recv looped', cnt)
    #     # print(topic, msg)
    #
    #     return topic, msg


# class ServiceProvider(Base):
#     """
#     Provides a service
#     """
#     def __init__(self, bind_to):
#         Base.__init__(self)
#         self.socket = self.ctx.socket(zmq.REP)
#         # tcp = 'tcp://' + bind_to[0] + ':' + str(bind_to[1])
#         tcp = self.getAddress(bind_to)
#         self.socket.bind(tcp)
#
#     def __del__(self):
#         self.socket.close()
#         self._stop()
#
#     def listen(self, callback):
#         # print 'listen'
#         while True:
#             jmsg = self.socket.recv()
#             msg = json.loads(jmsg)
#
#             ans = callback(msg)
#
#             jmsg = json.dumps(ans)
#             self.socket.send(jmsg)
#
#
# class ServiceClient(Base):
#     """
#     Client socket to get a response back from a service provider
#     """
#     def __init__(self, bind_to):
#         Base.__init__(self)
#         self.socket = self.ctx.socket(zmq.REQ)
#         # tcp = 'tcp://' + bind_to[0] + ':' + str(bind_to[1])
#         tcp = self.getAddress(bind_to)
#         self.socket.connect(tcp)
#
#     def __del__(self):
#         self.socket.close()
#         self._stop()
#
#     def get(self, msg):
#         jmsg = json.dumps(msg)
#         self.socket.send(jmsg)
#         jmsg = self.socket.recv()
#         msg = json.loads(jmsg)
#         return msg
