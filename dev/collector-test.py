#!/usr/bin/env python3

from __future__ import print_function, division
# from the_collector import BagReader, BagWriter

# fix path for now
import sys
sys.path.append("../")
from the_collector.messages import Messages
from the_collector.messages import Vector
from the_collector.messages import IMU

from pygecko.transport import Pub, Sub
from pygecko.transport import zmqTCP, GeckoCore
import multiprocessing as mp
import time

def publisher(e, topic):
    mm = Messages()
    p = Pub(pack=mm.serialize)
    addr = zmqTCP('localhost', 9998)
    p.connect(addr)
    name = mp.current_process().name
    try:
        cnt = 0
        while e.is_set():
            msg = IMU(Vector(1,2,3),Vector(1,2,3),Vector(1,2,3))
            p.pub(topic, msg)  # topic msg
            cnt += 1
            print(name, 'published msg on', topic)
            time.sleep(1)
    except Exception:
        pass
    print("*"*30)
    print('*** {} pub bye'.format(name))
    print("*"*30)


def subscriber(e, topic):
    mm = Messages()
    s = Sub(topics=[topic], unpack=mm.deserialize)
    addr = zmqTCP('localhost', 9999)
    s.connect(addr)
    name = mp.current_process().name
    try:
        while e.is_set():
            t, msg = s.recv()
            # print(s.recv(flags=zmq.NOBLOCK))
            # print("recv[{}]: {}".format(*s.recv()))
            # print(name, 'recvd message')
            print('{} recvd[{}] message'.format(name, t, msg))
    except Exception as e:
        print(e)
        pass
    print("*"*30)
    print('*** {} Sub bye'.format(name))
    print("*"*30)


if __name__ == '__main__':
    e = mp.Event()
    e.set()

    core = GeckoCore()

    procs = []

    p = mp.Process(target=publisher, args=(e, 'bob'), name='bob-publisher')
    p.start()
    procs.append(p)

    p = mp.Process(target=publisher, args=(e, 'sally'), name='sally-publisher')
    p.start()
    procs.append(p)

    p = mp.Process(target=subscriber, args=(e, 'bob'), name='bob-subscriber')
    p.start()
    procs.append(p)

    p = mp.Process(target=subscriber, args=(e, 'sally'), name='sally-1-subscriber')
    p.start()
    procs.append(p)

    p = mp.Process(target=subscriber, args=(e, 'sally'), name='sally-2-subscriber')
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
        print("<<< killing {} {} >>>".format(p.name, p.pid))
        p.join(1)

        # if you kill the publisher before the subscriber, the sub gets stuck
        # because recv() is blocking
        if p.is_alive():
            print('Crap, {} is still alive, terminate!'.format(p.name))
            p.terminate()
            p.join(0.1)
    core.join(1)
    exit()
