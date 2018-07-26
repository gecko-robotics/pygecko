#!/usr/bin/env python3
from __future__ import print_function
import multiprocessing as mp
import time
import signal
# fix path for now
import sys
sys.path.append("../../")

from pygecko.transport import Pub, Sub
from pygecko.transport import zmqTCP, GeckoCore


def gecko_setup():
    # kill -l
    # signal.signal(signal.SIGINT, signal_handler)
    # signal.signal(signal.SIGTERM, signal_handler)
    def signal_handler(signalnum, stackframe):
        # print('ignore ctrl-c signal:', signalnum)
        pass
    signal.signal(signal.SIGINT, signal_handler)


def publish(ns, e, **kwargs):
    if kwargs.get('signal', False):
        gecko_setup()

    topic = kwargs.get('topic', 'test')

    p = Pub()
    addr = zmqTCP('localhost', 9998)
    p.connect(addr)
    try:
        cnt = 0
        while e.is_set():
            msg = {'a': cnt, 'b': bytearray([1, 2, 3])}
            p.pub(topic, msg)  # topic msg
            cnt += 1
            print('>> published msg on topic {}'.format(topic))
            time.sleep(1)
    except Exception:
        pass
    print('pub bye ...')


def subscribe(ns, e, **kwargs):
    if kwargs.get('signal', False):
        gecko_setup()

    topic = kwargs.get('topic', 'test')
    s = Sub(topics=[topic])
    addr = zmqTCP('localhost', 9999)
    s.connect(addr)
    try:
        while e.is_set():
            # print(s.recv(flags=zmq.NOBLOCK))
            print("<< recv[{}]: {}".format(*s.recv()))
    except Exception as e:
        print(e)
        pass
    print('sub bye ...')


if __name__ == "__main__":
    # from multiprocessing.managers import SyncManager
    # mgr = SyncManager(address=address, authkey=authkey)
    # mgr.start()
    mgr = mp.Manager()
    ns = mgr.Namespace()
    e = mp.Event()
    e.set()
    kw = {'a':1, 'b':2}
    runable_process(ns, e)
    # runable_process({'ns':1, 'e':e, 'bob':5})
