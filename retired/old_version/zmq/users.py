#!/usr/bin/env python

from __future__ import print_function
from pygecko.ZmqClass import Pub, Sub
from pygecko.ZmqClass import Core, zmqTCP, GeckoCore
import multiprocessing as mp
import time


def publisher(e, topic):
    p = Pub()
    addr = zmqTCP('dalek.local', 9998)
    p.connect(addr)
    try:
        cnt = 0
        while e.is_set:
            msg = {'a': cnt, 'b': bytearray([1, 2, 3])}
            p.pub(topic, msg)  # topic msg
            cnt += 1
            print('published msg')
            # time.sleep(1)
    except Exception:
        pass
    print('pub bye ...')


def subscriber(e, topic):
    s = Sub(topics=[topic])
    addr = zmqTCP('localhost', 9999)
    s.connect(addr)
    try:
        while e.is_set:
            # print(s.recv(flags=zmq.NOBLOCK))
            print("recv[{}]: {}".format(*s.recv()))
    except Exception as e:
        print(e)
        pass
    print('sub bye ...')


if __name__ == '__main__':
    e = mp.Event()
    e.set()

    core = GeckoCore()

    procs = []

    p = mp.Process(target=publisher, args=(e, 'bob'), name='publisher')
    p.start()
    procs.append(p)

    p = mp.Process(target=publisher, args=(e, 'sally'), name='publisher')
    p.start()
    procs.append(p)

    p = mp.Process(target=subscriber, args=(e, 'bob'), name='subscriber')
    p.start()
    procs.append(p)

    p = mp.Process(target=subscriber, args=(e, 'sally'), name='subscriber')
    p.start()
    procs.append(p)

    p = mp.Process(target=subscriber, args=(e, 'sally'), name='subscriber')
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

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('ctrl-c')
            break

    e.clear()
    time.sleep(1)
    for p in procs:
        print("killing", p.name, p.pid)
        p.join()
    core.join()
