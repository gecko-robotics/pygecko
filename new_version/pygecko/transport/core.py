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
#
# kevin@Dalek ~ $ pstree -s zmq
# -+= 00001 root /sbin/launchd
#  \--- 17535 kevin /usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Ve
# kevin@Dalek ~ $ kill -9 17535
#

from __future__ import print_function
from __future__ import division
import zmq
from zmq.devices import ProcessProxy
import multiprocessing as mp
import time
# import socket as Socket
from pygecko.transport.helpers import zmqTCP, zmqUDS
from pygecko.transport.zmqclass import Pub, Sub
import signal


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

        print('+', '-'*30, sep='')
        print('| Core')
        print('+', '-'*30, sep='')
        # print("core:", core)
        print('|  In[sub]: {}'.format(inaddr))
        print('|  Out[pub]: {}'.format(outaddr))
        print('+', '-'*30, sep='')

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


class SignalCatch(object):
    """
    Catches SIGINT and SIGTERM signals and sets kill = True

    https://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully
    """
    kill = False
    def kill_signals(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        # signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self,signum, frame):
        self.kill = True
        print("got", signum, "kill =", self.kill)


class GProcess(object):
    ps = None
    def __del__(self):
        if self.ps:
            self.join(1)

    def run(self):
        raise NotImplementedError("Please subclass this class")

    def start(self):
        self.ps = mp.Process(name="GProcessProxy", target=self.run)
        self.ps.start()
        print(self.ps.name, self.ps.pid)

    def join(self, timeout=None):
        if self.ps:
            self.ps.join(timeout)
            if self.ps.is_alive():
                self.ps.terminate()
        self.ps = None


class GProcessProxy(SignalCatch, GProcess):
    def __init__(self, in_addr=None, out_addr=None):
        if in_addr is None:
            in_addr = zmqTCP('localhost', 9998)
        if out_addr is None:
            out_addr = zmqTCP('localhost', 9999)

        print(">> Core inputs {}".format(in_addr))
        print(">> Core Outputs {}".format(out_addr))

        self.ins = Sub()
        self.ins.bind(in_addr)

        self.outs = Pub()
        self.outs.bind(out_addr)

    def run(self):
        self.kill_signals()
        self.topics = {}
        cnt = 0
        while not self.kill:
            # time.sleep(1)
            print('ins: {}'.format(self.ins))
            msg = None
            while not msg:
                try:
                    topic, msg = self.ins.recv(flags=zmq.NOBLOCK)
                except Exception as e:
                    print(e)
                    pass

            print('>> Core: {}: {}'.format(topic, msg))

            self.outs.pub(topic, msg)

            # if topic not in self.topics.keys():
            #     self.topics[topic] = 0
            #
            # self.topics[topic] += 1
            #
            # cnt += 1
            # if cnt % 10:
            #     print('-'*30)
            #     for k,v in self.topics.items():
            #         print(' {} {} msgs'.format(k, v))

        print("proxy bye ...")
        return
