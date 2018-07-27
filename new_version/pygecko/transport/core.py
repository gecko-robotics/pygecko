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

# +------------------------------------------------------------
# | GeckoCore[24295].............. cpu:   6.6%    mem:   0.06%
# | [pconn(fd=18, family=<AddressFamily.AF_INET: 2>, type=1, laddr=addr(ip='192.168.86.213', port=9998), raddr=(), status='LISTEN'), pconn(fd=29, family=<AddressFamily.AF_INET: 2>, type=1, laddr=addr(ip='192.168.86.213', port=9999), raddr=(), status='LISTEN'), pconn(fd=30, family=<AddressFamily.AF_INET: 2>, type=1, laddr=addr(ip='192.168.86.213', port=9998), raddr=addr(ip='192.168.86.213', port=54466), status='ESTABLISHED'), pconn(fd=31, family=<AddressFamily.AF_INET: 2>, type=1, laddr=addr(ip='192.168.86.213', port=9999), raddr=addr(ip='192.168.86.213', port=54467), status='ESTABLISHED'), pconn(fd=32, family=<AddressFamily.AF_INET: 2>, type=1, laddr=addr(ip='192.168.86.213', port=9998), raddr=addr(ip='192.168.86.213', port=54468), status='ESTABLISHED'), pconn(fd=33, family=<AddressFamily.AF_INET: 2>, type=1, laddr=addr(ip='192.168.86.213', port=9999), raddr=addr(ip='192.168.86.213', port=54469), status='ESTABLISHED'), pconn(fd=34, family=<AddressFamily.AF_INET: 2>, type=1, laddr=addr(ip='192.168.86.213', port=9999), raddr=addr(ip='192.168.86.213', port=54470), status='ESTABLISHED'), pconn(fd=35, family=<AddressFamily.AF_INET: 2>, type=1, laddr=addr(ip='192.168.86.213', port=9999), raddr=addr(ip='192.168.86.213', port=54471), status='ESTABLISHED'), pconn(fd=36, family=<AddressFamily.AF_INET: 2>, type=1, laddr=addr(ip='192.168.86.213', port=9999), raddr=addr(ip='192.168.86.213', port=54472), status='ESTABLISHED'), pconn(fd=37, family=<AddressFamily.AF_INET: 2>, type=1, laddr=addr(ip='192.168.86.213', port=9999), raddr=addr(ip='192.168.86.213', port=54473), status='ESTABLISHED'), pconn(fd=38, family=<AddressFamily.AF_INET: 2>, type=1, laddr=addr(ip='192.168.86.213', port=9998), raddr=addr(ip='192.168.86.213', port=54474), status='ESTABLISHED')]
# | Total messages seen: 806
# +------------------------------
#  hello.........................   39.0 msgs/s      2.3 kB/s
#  hey there.....................   39.4 msgs/s      2.3 kB/s
#  cv............................   14.9 msgs/s   4467.5 kB/s
# ^C>> GeckoCore[24295] is shutdown

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
import psutil
import os


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
        # self.process = psutil.Process(self.ps.pid)

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
            self.topics[topic] = [0, 0]
            print('>> New topic: {}'.format(topic))

        self.topics[topic][0] += 1
        self.topics[topic][1] += bytes/(1024)  # kilobytes

    def keys(self):
        return self.topics.keys()

    def __getitem__(self, key):
        """
        only get one key, note, it resets the counts
        """
        ret = tuple(self.topics[key])
        self.topics[key] = [0, 0]
        return ret

    def get(self):
        """
        get an entire copy, note, it resets the entire database of counts
        """
        cp = self.topics.copy()
        for k,v in self.topics.items():
            self.topics[k] = [0, 0]
        return cp


class Performance(object):
    def __init__(self):
        self.ps.Process(os.getpid())
    def get(self):
        pd = ps.as_dict(attrs=['connections','cpu_percent','memory_percent'])
        label = '{}[{}]'.format(p.name, p.pid)
        print('| {:.<30} cpu: {:5}%    mem: {:6.2f}%'.format(label, pd['cpu_percent'], pd['memory_percent']))


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

        # self.process = psutil.Process(os.getpid())

    def socket_setup(self):

        print(">> Core inputs {}".format(self.in_addr))
        print(">> Core Outputs {}".format(self.out_addr))

        self.ins = Sub()
        self.ins.bind(self.in_addr)

        self.outs = Pub()
        self.outs.bind(self.out_addr)

    def run(self):
        self.kill_signals()  # have to setup signals in new process
        process = psutil.Process(self.ps.pid)

        print(">> Starting up GeckoCore")

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
        datumn = time.time()
        while not self.kill:
            # topic, msg = self.ins.raw_recv()

            # non-blocking so we can always check to see if there is a kill
            # signal to handle
            msg = None
            # while not msg:
            try:
                topic, msg = self.ins.raw_recv(flags=zmq.NOBLOCK)
            except Exception as e:
                # print(e)
                if self.kill:
                    return
                time.sleep(0.005)
                # continue

            if msg:
                topic = topic.decode('utf-8')  # FIXME

                self.outs.raw_pub(topic, msg)

                mc.touch(topic, len(msg))

            delta = time.time() - datumn
            if delta > 3:
                pd = process.as_dict(attrs=['connections','cpu_percent','memory_percent'])
                label = '{}[{}]'.format("GeckoCore", process.pid)
                print('+', '-'*60, sep='')
                print('| {:.<30} cpu: {:5}%    mem: {:6.2f}%'.format(label, pd['cpu_percent'], pd['memory_percent']))
                print('| Total messages seen: {}'.format(mc.total_msgs))
                print('+', '-'*30, sep='')
                for con in pd['connections']:
                    # print(con)
                    addr = con.laddr
                    # print(addr)
                    lip, lport = addr
                    addr = con.raddr
                    if addr:
                        rip, rport = addr
                    else:
                        rip, rport = (None, None)
                    print('| {} {}:{} connected to {}:{}'.format(con.status, lip, lport, rip, rport))
                print('+', '-'*30, sep='')
                for k in mc.keys():
                    count, bytes = mc[k]
                    print(' {:.<30} {:6.1f} msgs/s {:8.1f} kB/s'.format(k, count/delta, bytes/delta))
                datumn = time.time()
