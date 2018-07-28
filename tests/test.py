from __future__ import print_function

try:
    import pygecko
except ImportError:
    # fix path for now
    import sys
    sys.path.append("../")
    import pygecko

from pygecko.transport import Pub, Sub
from pygecko.transport import zmqTCP, zmqUDS, GeckoCore
from pygecko import FileJson, FileYaml
from pygecko.test import GeckoSimpleProcess

from the_collector.messages import Messages
from the_collector.messages import Vector
from the_collector.messages import IMU

import multiprocessing as mp
import os
import time
from math import pi


def file_func(Obj, fname):
    data = {'a':1, 'bob':[1,2,3,4], 'c':"hello cowboy", 'd': {'a':pi}}
    f = Obj()
    f.set(data)
    f.write(fname)
    d = f.read(fname)
    assert d == data
    os.remove(fname)


def test_json():
    file_func(FileJson, 'test.json')


def test_yaml():
    file_func(FileYaml, 'test.yml')


# tcp setup
tcp_pub = zmqTCP('localhost', 9998)
tcp_sub = zmqTCP('localhost', 9999)

# unix domain setup
uds_ifile = zmqUDS('/tmp/uds_ifile')
uds_ofile = zmqUDS('/tmp/uds_ofile')


def msg_zmq(pub_addr, sub_addr):
    # start message hub
    core = GeckoCore(pub_addr, sub_addr)
    core.start()

    def publisher(**kwargs):
        addr = kwargs.get('addr')
        messages = Messages()
        p = Pub(pack=messages.serialize)
        p.connect(addr)
        time.sleep(1)
        msg = Vector(1,2,3)
        p.pub('test', msg)  # topic msg

    args = {'addr': pub_addr}
    p = GeckoSimpleProcess()
    p.start(func=publisher, name='publisher', kwargs=args)

    # subscriber
    messages = Messages()
    s = Sub(topics=['test'], unpack=messages.deserialize)
    s.connect(sub_addr)
    t, msg = s.recv()

    print(t, msg)

    assert t == b'test'  # FIXME: fix stupid binary string crap!
    assert msg == Vector(1,2,3)

    p.join(0.1)
    core.join(0.1)


def test_msg_zmq_uds():
    msg_zmq(uds_ifile, uds_ofile)


def test_msg_zmq_tcp():
    msg_zmq(tcp_pub, tcp_sub)


def py_zmq(pub_addr, sub_addr):
    # start message hub
    core = GeckoCore(pub_addr, sub_addr)
    core.start()

    def publisher(**kwargs):
        addr = kwargs.get('addr')
        p = Pub()
        p.connect(addr)
        time.sleep(1)
        msg = {'a':1, 'b':[1,2,3], 'c':'hello cowboy'}
        p.pub('test', msg)  # topic msg

    args = {'addr': pub_addr}
    p = GeckoSimpleProcess()
    p.start(func=publisher, name='publisher', kwargs=args)

    # subscriber
    s = Sub(topics=['test'])
    s.connect(sub_addr)
    t, msg = s.recv()

    print(t, msg)

    assert t == b'test'
    assert msg == {'a':1, 'b':[1,2,3], 'c':'hello cowboy'}

    p.join(0.1)
    core.join(0.1)


def test_py_zmq_tcp():
    py_zmq(tcp_pub, tcp_sub)


def test_py_zmq_uds():
    py_zmq(uds_ifile, uds_ofile)


# def py_geckpy(pub_addr, sub_addr):
#     # start message hub
#     core = GeckoCore(pub_addr, sub_addr)
#     core.start()
#
#     geckopy = GeckoPy()
#
#     def callback(t, msg):
#         assert t == b'test'
#         assert msg == {'a':1, 'b':[1,2,3], 'c':'hello cowboy'}
#
#     def callback(**kwargs):
#         addr = kwargs.get('addr')
#         p = Pub()
#         p.connect(addr)
#         time.sleep(1)
#         msg = {'a':1, 'b':[1,2,3], 'c':'hello cowboy'}
#         p.pub('test', msg)  # topic msg
#
#
#
#     args = {'addr': pub_addr}
#     p = GeckoSimpleProcess()
#     p.start(func=publisher, name='publisher', kwargs=args)
#
#     # subscriber
#     s = Sub(topics=['test'])
#     s.connect(sub_addr)
#     t, msg = s.recv()
#
#     print(t, msg)
#
#     assert t == b'test'
#     assert msg == {'a':1, 'b':[1,2,3], 'c':'hello cowboy'}
#
#     p.join(0.1)
#     core.join(0.1)
#
# def test_py_geckopy_tcp():
#     py_geckpy(tcp_pub, tcp_sub)
#
#
# def test_py_geckopy_uds():
#     py_geckpy(uds_ifile, uds_ofile)