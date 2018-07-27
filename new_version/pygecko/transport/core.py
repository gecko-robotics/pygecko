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


class SignalCatch(object):
    """
    Catches SIGINT and SIGTERM signals and sets kill = True

    https://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully
    """
    kill = False
    def kill_signals(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self,signum, frame):
        self.kill = True
        # print(">> Got signal[{}], kill = {}".format(signum, self.kill))


class GProcess(object):
    ps = None
    name = None
    def __del__(self):
        if self.ps:
            self.join(1)

    def run(self):
        raise NotImplementedError("Please subclass this class")

    def start(self):
        if self.name is None:
            self.name = 'GProcess'
        self.ps = mp.Process(name=self.name, target=self.run)
        self.ps.start()
        print('>> Starting {}[{}]'.format(self.ps.name, self.ps.pid))

    def join(self, timeout=None):
        if self.ps:
            self.ps.join(timeout)
            if self.ps.is_alive():
                self.ps.terminate()
                print(">> Have to terminate {}[{}]".format(self.ps.name, self.ps.pid))
        print(">> {}[{}] is shutdown".format(self.ps.name, self.ps.pid))
        self.ps = None


class MsgCounter(object):
    """
    Simple class for keeping track of performance, how many messages per topic
    has it seen for a given starting point in time.
    """
    topics = {}
    total_msgs = 0
    def touch(self, topic, bytes=0):
        self.total_msgs += 1

        if topic not in self.topics.keys():
            # [msg_count, bytes, ]
            self.topics[topic] = [0, 0, time.time()]

        self.topics[topic][0] += 1
        self.topics[topic][1] += bytes/(1024)  # kilobytes

    def keys(self):
        return self.topics.keys()

    def __getitem__(self, key):
        return tuple(self.topics[key])

    def get(self):
        cp = self.topics.copy()
        tm = time.time()
        for k,v in self.topics.items():
            self.topics[k] = [0, 0, tm]
        return cp


class GeckoCore(SignalCatch, GProcess):
    """
    This is the main hub through which all messages travel. All though this is
    a point of failure, it allows us to have some metrics on performance.
    """
    def __init__(self, in_addr=None, out_addr=None):
        if in_addr is None:
            in_addr = zmqTCP('localhost', 9998)
        if out_addr is None:
            out_addr = zmqTCP('localhost', 9999)

        self.in_addr = in_addr
        self.out_addr = out_addr

        self.name = "GeckoCore"

    def socket_setup(self):

        print(">> Core inputs {}".format(self.in_addr))
        print(">> Core Outputs {}".format(self.out_addr))

        self.ins = Sub()
        self.ins.bind(self.in_addr)

        self.outs = Pub()
        self.outs.bind(self.out_addr)

    def run(self):
        self.kill_signals()  # have to setup signals in new process

        try:
            self.socket_setup()  # have to setup sockets in new process
        except zmq.error.ZMQError as e: # typicall gets called if addr in use
            err_msg = "*** {} ***".format(e)
            print('*'*len(err_msg))
            print('*'*len(err_msg))
            print(err_msg)
            print('*'*len(err_msg))
            print('*'*len(err_msg))
            exit(1)

        # datumn = time.time()
        mc = MsgCounter()
        while not self.kill:
            # topic, msg = self.ins.raw_recv()

            # non-blocking so we can always check to see if there is a kill
            # signal to handle
            msg = None
            while not msg:
                try:
                    topic, msg = self.ins.raw_recv(flags=zmq.NOBLOCK)
                except Exception as e:
                    # print(e)
                    if self.kill:
                        return
                    time.sleep(0.005)
                    continue

            topic = topic.decode('utf-8')

            self.outs.raw_pub(topic, msg)

            mc.touch(topic, len(msg))

            if mc.total_msgs % 100 == 0:
                print('-'*30)
                print(' Total messages seen: {}'.format(mc.total_msgs))
                for k in mc.keys():
                    count, bytes, datumn = mc[k]
                    delta = time.time() - datumn
                    print(' {} {} msgs in {:.2f} sec {:.2f} msgs/sec    {:.1f} kB/sec'.format(k, count, delta, count/delta, bytes/delta))
