from __future__ import print_function

# fix path for now
import sys
sys.path.append("../")

from pygecko.transport import Pub, Sub
from pygecko.transport import zmqTCP, zmqUDS, GeckoCore
from pygecko import FileJson, FileYaml

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
    # print('d', d)
    # print('data', data)
    assert d == data
    os.remove(fname)


def test_json():
    file_func(FileJson, 'test.json')


def test_yaml():
    file_func(FileYaml, 'test.yml')


tcp_core = GeckoCore()

# dir = os.path.dirname(os.path.abspath(__file__))
# uds_file = zmqUDS(dir + '/uds_file')
# print(uds_file)
# uds_core = GeckoCore(uds_file, uds_file)


def msg_zmq(pub_addr, sub_addr):
    def publisher(addr):
        messages = Messages()
        p = Pub(pack=messages.serialize)
        # addr = zmqTCP('localhost', 9998)
        p.connect(addr)
        time.sleep(1)
        msg = Vector(1,2,3)
        p.pub('test', msg)  # topic msg

    p = mp.Process(target=publisher, args=(pub_addr,), name='publisher')
    p.start()

    # subscriber
    messages = Messages()
    s = Sub(topics=['test'], unpack=messages.deserialize)
    # addr = zmqTCP('localhost', 9999)
    s.connect(sub_addr)
    t, msg = s.recv()

    print(t, msg)

    assert t == b'test'
    assert msg == Vector(1,2,3)

    p.join(0.1)
    if p.is_alive():
        print('Crap, {} is still alive, terminate!'.format(p.name))
        p.terminate()
        p.join(0.1)



# def test_msg_zmq_uds():
#     dir = os.path.dirname(os.path.abspath(__file__))
#     f = zmqUDS(dir + '/uds_file')
#     msg_zmq(f, f)


def test_msg_zmq_tcp():
    msg_zmq(zmqTCP('localhost', 9998), zmqTCP('localhost', 9999))\


def py_zmq(pub_addr, sub_addr):
    def publisher(addr):
        # addr = zmqTCP('localhost', 9998)
        p = Pub()
        p.connect(addr)
        time.sleep(1)
        msg = {'a':1, 'b':[1,2,3], 'c':'hello cowboy'}
        p.pub('test', msg)  # topic msg

    p = mp.Process(target=publisher, args=(pub_addr,), name='publisher')
    p.start()

    # subscriber
    s = Sub(topics=['test'])
    # addr = zmqTCP('localhost', 9999)
    s.connect(sub_addr)
    t, msg = s.recv()

    print(t, msg)

    assert t == b'test'
    assert msg == {'a':1, 'b':[1,2,3], 'c':'hello cowboy'}

    p.join(0.1)
    if p.is_alive():
        print('Crap, {} is still alive, terminate!'.format(p.name))
        p.terminate()
        p.join(0.1)



def test_py_zmq_tcp():
    py_zmq(zmqTCP('localhost', 9998), zmqTCP('localhost', 9999))


# def test_py_zmq_uds():
#     py_zmq(uds_file, uds_file)
