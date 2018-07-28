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
from pygecko.transport import zmqTCP, GeckoCore, zmqUDS
from pygecko.multiprocessing import GeckoPy

import numpy as np

import multiprocessing as mp
import time
import signal
import os


class GSimpleProcess(object):
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

    def start(self, func, name='simple_process', **kwargs):
        self.ps = mp.Process(name=name, target=func, **kwargs)
        self.ps.start()
        print('>> Started: {}[{}]'.format(self.ps.name, self.ps.pid))

    def join(self, timeout=None):
        print('>> Stopping {}[{}] ...'.format(self.ps.name, self.ps.pid), end=' ')
        if self.ps:
            self.ps.join(timeout)
            if self.ps.is_alive():
                self.ps.terminate()
        self.ps = None
        print('stopped')


def publish(**kwargs):
    geckopy = GeckoPy()
    rate = geckopy.Rate(2)

    print('pub', kwargs)

    topic = kwargs.get('topic', 'test')
    fname = kwargs.get('pub_uds', None)
    print('fname', fname)

    p = geckopy.Publisher(uds_file=fname)

    while not geckopy.is_shutdown():
        msg = {'s': time.time()}
        p.pub(topic, msg)  # topic msg

        rate.sleep()

    print('pub bye ...')


def subscribe(**kwargs):
    geckopy = GeckoPy()

    def f(t, m):
        print('>> Message[{}]'.format(t))

    topic = kwargs.get('topic', 'test')
    fname = kwargs.get('sub_uds')

    s = geckopy.Subscriber([topic], f, uds_file=fname)
    geckopy.spin(20)
    print('sub bye ...')


if __name__ == '__main__':
    procs = []
    args = {
        'topic': 'hi',
        'sub_uds': '/tmp/uds_ofile',
        'pub_uds': '/tmp/uds_ifile',
    }

    # this is sort of like crossing RX/TX lines here
    #        +---------+
    # pub -> | in  out | -> sub
    #        +---------+
    core = GeckoCore(
        in_addr=zmqUDS(args['pub_uds']),
        out_addr=zmqUDS(args['sub_uds'])
    )
    core.start()

    # p = mp.Process(target=publish, name='publisher', kwargs=args)
    # p.start()
    # procs.append(p)
    # print('>> Started: {}[{}]'.format(p.name, p.pid))
    p = GSimpleProcess()
    p.start(func=publish, name='publisher', kwargs=args)
    procs.append(p)

    p = mp.Process(target=subscribe, name='subscriber', kwargs=args)
    p.start()
    procs.append(p)
    print('>> Started: {}[{}]'.format(p.name, p.pid))

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('main process got ctrl-c')
            break

    for p in procs:
        print(">> joining", p.name, p.pid)
        p.join(0.1)
        if p.is_alive():
            print(">> Have to terminate() {}[{}]".format(p.name, p.pid))
            p.terminate()
    core.join(0.1)


# class GeckoMP(object):
#     def __init__(self, sig=True, log=None):
#         if signal:
#             signal.signal(signal.SIGINT, self.signal_handler)
#
#     @staticmethod
#     def signal_handler(signalnum, stackframe):
#         # print('ignore ctrl-c signal:', signalnum)
#         pass
#
# #----------------------------------------------
# class GProcess(object):
#     ps = None
#
#     def __del__(self):
#         if self.ps:
#             self.join(1)
#
#     @property
#     def name(self):
#         return self.ps.name
#
#     @property
#     def pid(self):
#         return self.ps.pid
#
#     def is_alive(self):
#         if self.ps:
#             return self.ps.is_alive()
#         else:
#             return False
#
#     def terminate(self):
#         if self.ps:
#             self.ps.terminate()
#
#     def run(self):
#         raise NotImplementedError("Please subclass this class")
#
#     def start(self, args=None, kwargs=None):
#         if args:
#             self.ps = mp.Process(name="GProcessProxy", target=self.run, args=args)
#         else:
#             raise Exception("need to finish start()")
#
#         self.ps.start()
#         print('>> Started: {}[{}]'.format(self.ps.name, self.ps.pid))
#
#     def join(self, timeout=None):
#         if self.ps:
#             self.ps.join(timeout)
#             if self.ps.is_alive():
#                 self.ps.terminate()
#         self.ps = None


# class SignalCatch(object):
#     """
#     Catches SIGINT and SIGTERM signals and sets kill = True
#
#     https://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully
#     """
#     kill = False
#     def kill_signals(self):
#         signal.signal(signal.SIGINT, self.exit_gracefully)   # ctl-C
#         signal.signal(signal.SIGTERM, self.exit_gracefully)  # program termination
#
#     def exit_gracefully(self,signum, frame):
#         self.kill = True
#         print("got", signum, "kill =", self.kill)
