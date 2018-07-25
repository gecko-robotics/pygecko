#!/usr/bin/env python3

from __future__ import print_function

# fix path for now
import sys
sys.path.append("../")

from pygecko.transport import Pub, Sub
from pygecko.transport import zmqTCP, GeckoCore

from the_collector.messages import Messages
from the_collector.messages import Vector
from the_collector.messages import IMU
from the_collector import BagWriter

import multiprocessing as mp
import os
import time


def publisher(e, topic):
    messages = Messages()
    p = Pub(pack=messages.serialize)
    addr = zmqTCP('localhost', 9998)
    p.connect(addr)
    name = mp.current_process().name
    try:
        cnt = 0
        while e.is_set():
            msg = IMU(Vector(1,2,3),Vector(1,2,3),Vector(1,2,3))
            p.pub(topic, msg)  # topic msg
            cnt += 1
            print('>> {} published msg on {}'.format(name, topic))
            time.sleep(1)
    except Exception:
        pass
    print("*"*30)
    print('*** {} pub bye'.format(name))
    print("*"*30)


def subscriber(e, topic):
    messages = Messages()
    s = Sub(topics=[topic], unpack=messages.deserialize)
    filename = 'test.bag'
    bag = BagWriter(filename, buffer_size=10, pack=messages.serialize)
    addr = zmqTCP('localhost', 9999)
    s.connect(addr)
    name = mp.current_process().name
    try:
        while e.is_set():
            # print(s.recv(flags=zmq.NOBLOCK))
            # print("recv[{}]: {}".format(*s.recv()))
            t, msg = s.recv()
            print('<< {} recvd[{}] message'.format(name, t, msg))
            bag.push(t, msg)
    except Exception as e:
        print(e)
        bag.close()
    print("{} is {:.1f} kB".format(filename, os.path.getsize(filename)/1000))
    # os.remove(filename)
    print("*"*30)
    print('*** {} Sub bye'.format(name))
    print("*"*30)


if __name__ == '__main__':
    e = mp.Event()
    e.set()

    core = GeckoCore()

    procs = []

    p = mp.Process(target=publisher, args=(e, 'bob'), name='publisher')
    p.start()
    procs.append(p)

    p = mp.Process(target=subscriber, args=(e, 'bob'), name='subscriber')
    p.start()
    procs.append(p)

    # def signal_handler(signalnum, stackframe):
    #     print('ctrl-c signal.')
    #     e.clear()
    #     sys.exit(0)
    #
    # # kill -l
    # signal.signal(signal.SIGINT, signal_handler)
    # signal.signal(signal.SIGTERM, signal_handler)

    for _ in range(5):
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('ctrl-c')
            break

    e.clear()
    time.sleep(1)
    for p in procs:
        print("joining", p.name, p.pid)
        p.join(1)
        if p.is_alive():
            print('Crap, {} is still alive, terminate!'.format(p.name))
            p.terminate()
            p.join(0.1)
    core.join(1)
