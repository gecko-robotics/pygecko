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

from pygecko.gecko_enums import Status
from pygecko.gecko_enums import ZmqType
from pygecko.transport.helpers import zmqTCP
# from pygecko.transport.helpers import zmqUDS
# from pygecko.transport.zmq_sub_pub import Pub, Sub
from pygecko.transport.zmq_req_rep import Rep, Req
from pygecko.multiprocessing.geckopy import Rate
from pygecko.multiprocessing.sig import SignalCatch  # this one causes import problems!!
from pygecko.transport.helpers import GetIP
from pygecko.transport.helpers import zmq_version
import psutil
import os
import multiprocessing as mp
import time


class GProcess(object):
    """
    A class for setting up multiprocessing. It does nothing, but inheriting
    from it allows a child class to spawn processes.
    """
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


class ProcPerformance(object):
    """Keeps track of a process'es performance: memory, cpu, network connections"""
    def __init__(self):
        self.procs = {}
        self.datumn = time.time()
        # self.print_interval = print_interval

    def push(self, pid, name):
        self.procs[pid] = (psutil.Process(pid), name,)
        # print('*** push: {}[{}] ***'.format(name, pid))

    def pop(self, pid):
        try:
            self.procs.pop(pid)
        except Exception:
            # print('*** pop: {} ***'.format(e))
            pass

    def procprint(self):
        print('+'+'='*40)
        print('| Processes Performance')

        procs = tuple(self.procs.values())
        net = {}
        for ps, psname in procs:
            try:
                if ps.is_running():
                    # faster or better?
                    # p.cpu_percent(interval=None)
                    # p.memory_percent(memtype="rss")
                    pd = ps.as_dict(attrs=['connections','cpu_percent','memory_percent'])
                    net[psname] = pd['connections']
                    # print(psname, pd['connections'])
                    # cpu = ps.cpu_percent()
                    # cpu = cpu if cpu else -1
                    # mem = ps.memory_percent()
                    # mem = mem if mem else -1
                    label = '[{}] {}'.format(ps.pid, psname)
                    print('| {:.<30} cpu:{:5.1f}%  mem:{:5.1f}%'.format(label, pd['cpu_percent'], pd['memory_percent']))
                    # print('| {:.<30} cpu: {:5}%    mem: {:6.2f}%'.format(label, cpu, mem))
                else:
                    # print('*** remove {} ***'.format(ps.pid))
                    self.pop(ps.pid)
            except Exception:
                self.pop(ps.pid)

        print('+', '-'*30, sep='')
        print('| ESTABLISHED Connections')
        for name, p in net.items():
            for c in p:
                if c.status == 'ESTABLISHED':
                    if c.raddr:
                        rip, rport = c.raddr  # remote ip/port number
                    else:
                        rip, rport = (None, None,)
                    lip, lport = c.laddr
                    print('| {:.<20} {}:{} --> {}:{}'.format(name, lip, lport, rip, rport))

        print('+', '-'*30, sep='')
        print('| LISTEN Connections')
        for name, p in net.items():
            for c in p:
                if c.status == 'LISTEN':
                    lip, lport = c.laddr  # local ip/port number
                    print('| {:.<20} {}:{}'.format(name, lip, lport))



class GeckoCore(SignalCatch, GProcess):
    """
    This is the main hub through which all messages travel. All though this is
    a point of failure, it allows us to have some metrics on performance.
    """
    def __init__(self, port=11311, hertz=5):
        """
        in/out_port: port on localhost
        in/out_addr: full address string
        """
        self.ip = GetIP().get()
        self.pubs = {}
        self.port = port
        self.rep_addr = zmqTCP(self.ip, self.port)

        print('+'+'='*40)
        print('| GeckoCore')
        print('+'+'='*40)
        print("| {}".format(zmq_version()))
        print("| REP: {}".format(self.rep_addr))
        print('+'+'='*40)

        self.name = "GeckoCore"
        self.hertz = hertz
        self.print_interval = 3  # seconds

    def __del__(self):
        pass

    def handle_reply(self, data):
        ret = {}
        if data['T'] == ZmqType.pub:  # pub
            if type(data['topics']) is list:
                for t in data['topics']:
                    self.pubs[t] = data['addr']
            else:
                self.pubs[data['topics']] = data['addr']

            ret = {'status': Status.ok}

        elif data['T'] == ZmqType.sub:
            topic = data['topics'][0]
            if topic in self.pubs.keys():
                ret = {
                    'status': Status.ok,
                    'topics': topic,
                    'addr': self.pubs[topic]
                }
            else:
                return {'status': Status.topic_not_found}
        else:
            return {'status': Status.invalid_zmq_type}

        # print("<<< pid: {}   name: {} >>>".format(pid, name))
        # self.printTopics()

        pid = int(data['pid'])
        name = data['name']
        self.perf.push(pid, name)

        return ret

    def printTopics(self):
        print('+'+'='*40)
        print("| Published Topics <topic>@tcp://<ip>:<port>")
        i = 1
        for k,v in self.pubs.items():
            print("|{:3}: {}@{}".format(i,k,v))
            i+=1

    def run(self):
        """
        This is the main thread that answers req/rep connections to core.
        """
        self.kill_signals()  # have to setup signals in new process

        # process = psutil.Process(self.ps.pid)

        self.perf = ProcPerformance()
        self.perf.push(os.getpid(), "GeckoCore")

        # print(">> Starting up GeckoCore")

        reply = Rep()
        reply.bind(self.rep_addr)

        rate = Rate(self.hertz)

        # mc = MsgCounter()
        datumn = time.time()
        while not self.kill:
            # non-blocking so we can always check to see if there is a kill
            # signal to handle
            reply.listen_nb(self.handle_reply)

            # print proc performance
            delta = time.time() - datumn
            if delta > self.print_interval:
                self.perf.procprint()
                self.printTopics()
                datumn = time.time()

            rate.sleep()

        # print("** left main core loop ***")



##########################################################################

# class MsgCounter(object):
#     """
#     Simple class for keeping track of performance, how many messages per topic
#     has it seen for a given starting point in time.
#     """
#     def __init__(self):
#         self.topics = {}
#         self.total_msgs = 0
#         self.datumn = time.time()
#
#     def touch(self, topic, mbytes=0):
#         self.total_msgs += 1
#
#         # if topic not in self.topics.keys():
#         #     # [msg_count, bytes, ]
#         #     self.topics[topic] = [0, 0]
#         #     print('>> New topic: {}'.format(topic))
#
#         try:
#             self.topics[topic][0] += 1
#             self.topics[topic][1] += mbytes/(1024)  # kilobytes
#         except (NameError, KeyError):
#             self.topics[topic] = [1, mbytes/(1024)]
#
#     def dataprint(self, delta):
#         print('+', '-'*30, sep='')
#         print('| Topic Performance')
#         for key, val in self.topics.items():
#             count, mbytes = val
#             # the topic names (keys) should be binary strings, so need to
#             # convert into normal strings
#             print('| {:.<30} {:6.1f} msgs/s {:8.1f} kB/s'.format(key.decode('utf-8'), count/delta, mbytes/delta))
#
#             # reset msg,data count
#             self.topics[key] = [0, 0]
#
#         # reset datumn
#         self.datumn = time.time()
