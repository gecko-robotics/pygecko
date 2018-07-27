#!/usr/bin/env python3
#
# kevin@Dalek ~ $ pstree -s zmq
# -+= 00001 root /sbin/launchd
#  \--- 17535 kevin /usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Ve
# kevin@Dalek ~ $ kill -9 17535
#

from __future__ import print_function

# fix path for now
import sys
sys.path.append("../")

from pygecko.transport import Pub, Sub
from pygecko.transport import zmqTCP, GeckoCore

import numpy as np

import multiprocessing as mp
import time
import signal
import os

class GeckoMP(object):
    def __init__(self, sig=True, log=None):
        if signal:
            signal.signal(signal.SIGINT, self.signal_handler)

    @staticmethod
    def signal_handler(signalnum, stackframe):
        # print('ignore ctrl-c signal:', signalnum)
        pass

#----------------------------------------------
class GProcess(object):
    ps = None

    def __del__(self):
        if self.ps:
            self.join(1)

    @property
    def name(self):
        return self.ps.name

    @property
    def pid(self):
        return self.ps.pid

    def is_alive(self):
        if self.ps:
            return self.ps.is_alive()
        else:
            return False

    def terminate(self):
        if self.ps:
            self.ps.terminate()

    def run(self):
        raise NotImplementedError("Please subclass this class")

    def start(self, args=None, kwargs=None):
        if args:
            self.ps = mp.Process(name="GProcessProxy", target=self.run, args=args)
        else:
            raise Exception("need to finish start()")

        self.ps.start()
        print('>> Started: {}[{}]'.format(self.ps.name, self.ps.pid))

    def join(self, timeout=None):
        if self.ps:
            self.ps.join(timeout)
            if self.ps.is_alive():
                self.ps.terminate()
        self.ps = None


class SignalCatch(object):
    """
    Catches SIGINT and SIGTERM signals and sets kill = True

    https://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully
    """
    kill = False
    def kill_signals(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)   # ctl-C
        signal.signal(signal.SIGTERM, self.exit_gracefully)  # program termination

    def exit_gracefully(self,signum, frame):
        self.kill = True
        print("got", signum, "kill =", self.kill)


class PubPs(GProcess, SignalCatch):
    def run(self, topic):
        self.kill_signals()
        p = Pub()
        addr = zmqTCP('localhost', 9998)
        p.connect(addr)
        print('Publisher connected to: {}'.format(addr))
        cnt = 0
        raw_img = np.random.rand(640, 480)
        while not self.kill:
            msg = {'a': cnt, 'b': raw_img.tobytes(), 'c': time.time()}
            p.pub(topic, msg)  # topic msg
            cnt += 1
            # print('[{}] published msg'.format(cnt))
            time.sleep(0.05)
        print('pub bye ...')



def publisher(e, topic):
    gmp = GeckoMP()
    p = Pub()
    addr = zmqTCP('localhost', 9998)
    p.connect(addr)
    print('Publisher connected to: {}'.format(addr))
    cnt = 0
    while e.is_set():
        msg = {'a': cnt, 'b': bytearray([1, 2, 3])}
        p.pub(topic, msg)  # topic msg
        cnt += 1
        # print('[{}] published msg'.format(cnt))
        time.sleep(.05)
    print('pub bye ...')


def subscriber(e, topic):
    gmp = GeckoMP()
    s = Sub(topics=[topic])
    addr = zmqTCP('localhost', 9999)
    print('Subscriber connected to: {}'.format(addr))
    s.connect(addr)
    while e.is_set():
        # print(s.recv(flags=zmq.NOBLOCK))
        topic, msg = s.recv()
        # print("recv[{}]: {}".format(topic, msg))

    print('sub bye ...')


if __name__ == '__main__':
    print('>> Main process pid: {}'.format(os.getpid()))
    e = mp.Event()
    e.set()

    core = GeckoCore()
    # core = GProcessProxy()
    core.start()

    procs = []

    print('-'*30)

    p = PubPs()
    # p = mp.Process(target=publisher, args=(e, 'bob'), name='publisher')
    p.start(args=('tom',))
    procs.append(p)
    # print('>> Started: {}[{}]'.format(p.name, p.pid))

    p = mp.Process(target=publisher, args=(e, 'sally'), name='publisher')
    p.start()
    procs.append(p)


    p = mp.Process(target=publisher, args=(e, 'bob'), name='publisher')
    p.start()
    procs.append(p)

    p = mp.Process(target=subscriber, args=(e, 'bob'), name='subscriber')
    p.start()
    procs.append(p)
    print('>> Started: {}[{}]'.format(p.name, p.pid))

    print('-'*30)

    p = mp.Process(target=subscriber, args=(e, 'sally'), name='subscriber')
    p.start()
    procs.append(p)

    p = mp.Process(target=subscriber, args=(e, 'tom'), name='subscriber')
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
            print('main process got ctrl-c')
            break

    e.clear()
    time.sleep(0.1)
    for p in procs:
        print("killing", p.name, p.pid)
        p.join(0.1)
        if p.is_alive():
            print(">> Have to terminate() {}[{}]".format(p.name, p.pid))
            p.terminate()
    core.join(0.1)
