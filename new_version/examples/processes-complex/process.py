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
from math import sin, cos, pi, sqrt

import numpy as np


def chew_up_cpu():
    # chew up some cpu
    for i in range(90):
        m = sin(i*pi/180)*cos(i*pi/180)*sin(i*pi/180)*cos(i*pi/180)*sin(i*pi/180)*cos(i*pi/180)
        sqrt(m**9)


class GeckoMP(object):
    def __init__(self, sig=True, log=None):
        if signal:
            signal.signal(signal.SIGINT, self.signal_handler)

    @staticmethod
    def signal_handler(signalnum, stackframe):
        # print('ignore ctrl-c signal:', signalnum)
        pass


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
        # gecko_setup()
        gmp = GeckoMP(sig=True)

    topic = kwargs.get('topic', 'test')

    p = Pub()
    addr = zmqTCP('localhost', 9998)
    p.connect(addr, hwm=1)
    try:
        cnt = 0
        raw_img = np.random.rand(640, 480)  # HD (1920x1080) kills performance
        while e.is_set():
            img = raw_img.tobytes()
            ns.image = img
            msg = {'a': cnt, 'b': img, 's': time.time()}
            p.pub(topic, msg)  # topic msg
            cnt += 1
            # print('>> published msg on topic {}'.format(topic))

            # chew up some cpu
            # chew_up_cpu()
            time.sleep(.05)
    except Exception:
        pass
    print('pub bye ...')


def subscribe(ns, e, **kwargs):
    if kwargs.get('signal', False):
        gecko_setup()

    topic = kwargs.get('topic', 'test')
    s = Sub(topics=[topic])
    addr = zmqTCP('localhost', 9999)
    s.connect(addr, hwm=1)
    try:
        while e.is_set():
            # print(s.recv(flags=zmq.NOBLOCK))
            t, msg = s.recv()
            # print("<< recv[{}][{}]: {}".format(t, msg['a'], time.time() - msg['s']))
            # chew up some cpu
            chew_up_cpu()
            chew_up_cpu()
            chew_up_cpu()
            chew_up_cpu()

            # Holly crap namespace and pickle use a lot of cpu!
            # zmq hs only 23%, but syncmanager is 77%
            # ns == msg image True
            # +------------------------------
            # | Alive processes: 11
            # +------------------------------
            # | subscribe[19339].............. cpu: 12.2%    mem: 0.10%
            # | subscribe[19343].............. cpu: 13.7%    mem: 0.10%
            # | SyncManager-1[19327].......... cpu: 77.4%    mem: 0.19%
            # | subscribe[19338].............. cpu: 12.5%    mem: 0.10%
            # | subscribe[19341].............. cpu: 13.6%    mem: 0.10%
            # | publish[19336]................ cpu: 8.7%    mem: 0.40%
            # | GeckoCore[19328].............. cpu: 23.3%    mem: 0.11%
            # | subscribe[19344].............. cpu: 13.8%    mem: 0.10%
            # | subscribe[19342].............. cpu: 13.7%    mem: 0.11%
            # | publish[19337]................ cpu: 8.8%    mem: 0.40%
            # | subscribe[19340].............. cpu: 13.7%    mem: 0.10%
            # if 'b' in msg:
            #     print('ns == msg image', ns.image == msg['b'])

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
