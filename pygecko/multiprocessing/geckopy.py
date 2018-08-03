##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################
from pygecko.transport.zmq_base import ZMQError
from pygecko.transport.zmq_sub_pub import Pub, Sub  #, SubNB
from pygecko.transport.zmq_req_rep import Req
from pygecko.transport.helpers import zmqTCP, zmqUDS
from pygecko.transport.core import SignalCatch # capture signals in processes
import signal
import time
from colorama import Fore, Back, Style
import multiprocessing as mp

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


class GeckoRate(object):
    """
    Uses sleep to keep a desired rate.
    """
    def __init__(self, hertz):
        self.last_time = time.time()
        self.dt = 1/hertz

    def sleep(self):
        """
        This uses sleep to delay the function. If your loop is faster than your
        desired Hertz, then this will calculate the time difference so sleep
        keeps you close to you desired hertz. If your loop takes longer than
        your desired hertz, then it doesn't sleep.
        """
        now = time.time()
        diff = now - self.last_time
        if diff < self.dt:
            new_sleep = self.dt - diff
            time.sleep(new_sleep)

        # now that we hav slept a while, set the current time
        # as the last time
        self.last_time = time.time()


class GeckoPy(SignalCatch):
    """
    This class setups a function in a new process. It also provides some useful
    functions for other things.
    """
    def __init__(self, **kwargs):
        # print('pygecko', kwargs)
        # signal.signal(signal.SIGINT, self.signal_handler)
        # self.kill = False
        self.kill_signals()  # have to setup signals in new process
        self.subs = []   # subscriber nodes
        self.hooks = []  # functions to call on shutdown
        self.name = mp.current_process().name
        self.pid = mp.current_process().pid
        self.queue = kwargs.get('queue', None)

        # print(self.name, 'kwargs:\n{}'.format(kwargs))

        # don't we always have this???
        self.core_outaddr = kwargs.get('core_outaddr', None)
        self.core_inaddr = kwargs.get('core_inaddr', None)
        if self.core_inaddr:
            self.notify_core(True, self.core_inaddr)

    # def __del__(self):
    #     if self.core_addr:
    #         self._notify_core(False, addr)

    def log(self, msg):
        if self.queue:
            self.queue.put((self.pid, self.name, msg,))
        else:
            print(Fore.BLUE + '{}[{}]:'.format(self.name, self.pid) + Fore.RESET + '{}'.format(msg))

    def is_shutdown(self):
        return self.kill

    def Rate(self, hertz):
        return GeckoRate(hertz)

    def get_time(self):
        return time.time()

    def notify_core(self, status, addr=None):
        """
        Pass info to geckocore:
            {'proc_info': (pid, name, status)}

            psutil returns name as python for everything. It doesn't know about
            the multiprocessing.Process.name

            status:
                True: proc up and running
                False: proc is dead
        """
        # print("********** wtf *************")

        request = Req()
        request.connect(zmqTCP('localhost', 10000))

        ans = None
        msg = {'proc_info': (self.pid, self.name, status,)}

        while not ans:
            ans = request.get(msg)
            print("*** {} : {} ***".format(msg, ans))
            time.sleep(0.01)

        print("**** notify core:", ans)
        request.close()
        # time.sleep(5)

    # def Publisher(self, uds_file=None, host='localhost', queue_size=10, bind=False):
    def Publisher(self, addr=zmqTCP('localhost', 9998), queue_size=10, bind=False):
        p = Pub()
        if self.core_inaddr:
            addr = self.core_inaddr

        if bind:
            p.bind(addr, queue_size=queue_size)
        else:
            p.connect(addr, queue_size=queue_size)

        return p

    # def Subscriber(self, topics, cb, host='localhost', uds_file=None):
    def Subscriber(self, topics, cb_func, addr=zmqTCP('localhost', 9999)):
        s = Sub(cb_func=cb_func, topics=topics)
        if self.core_outaddr:
            addr = self.core_outaddr

        s.connect(addr)
        self.subs.append(s)

    def ServiceProxy(self, topic):
        return None

    def Service(self, topic, cb_func):
        s = Srv(topic, cb_func)
        s.connect(addr)

    def on_shutdown(self, hook):
        """
        Allows you to setup hooks for when eveything shuts down. Function accepts
        no arguments.

        hook = function()

        This is an array, so functions are called in order they were put in:
        FIFO.
        """
        self.hooks.append(hook)

    def spin(self, hertz=100):
        """

        """
        rate = self.Rate(1.2*hertz)
        while not self.kill:
            for sub in self.subs:
                sub.recv_nb()
            rate.sleep()
        if len(self.hooks) > 0:
            for h in self.hooks:
                h()
