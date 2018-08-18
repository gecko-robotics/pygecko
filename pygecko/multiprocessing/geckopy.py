##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################
from pygecko.transport.zmq_base import ZMQError
from pygecko.transport.zmq_sub_pub import Pub, Sub  #, SubNB
from pygecko.transport.zmq_req_rep import Req
from pygecko.transport.helpers import zmqTCP, zmqUDS
from pygecko.multiprocessing.sig import SignalCatch # capture signals in processes
# from pygecko.multiprocessing.delay import GeckoRate, Rate
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

g_geckopy = None



# import signal
#
#
# class SignalCatch(object):
#     """
#     Catches SIGINT and SIGTERM signals and sets kill = True
#
#     https://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully
#     """
#     kill = False
#     def kill_signals(self):
#         signal.signal(signal.SIGINT, self.exit_gracefully)
#         signal.signal(signal.SIGTERM, self.exit_gracefully)
#
#     def exit_gracefully(self, signum, frame):
#         """
#         When handler gets called, it sets the self.kill to True
#         """
#         self.kill = True
#         # print(">> Got signal[{}], kill = {}".format(signum, self.kill))

class Throttle(object):
    """
    value?
    """
    pass


class Rate(object):
    """
    Uses sleep to keep a desired message/sample rate.
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


# class Rate(GeckoRate):
#     pass


class GeckoPy(SignalCatch):
    """
    This class setups a function in a new process.
    """
    def __init__(self, **kwargs):
        """
        kwargs: can have a lot of things in it. Some common keys are:
            core_outaddr: tcp or uds address of geckocore outputs
            core_inaddr: tcp or uds address of geckocore inputs
            queue: multiprocessing.Queue for log messages
        """
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

        # sets default
        self.core_outaddr = kwargs.get(
            'core_outaddr',
            zmqTCP('localhost', 9999))

        self.core_inaddr = kwargs.get(
            'core_inaddr',
            zmqTCP('localhost', 9998))

        if self.core_inaddr:
            self.notify_core(True, self.core_inaddr)

    def __del__(self):
        if len(self.hooks) > 0:
            for h in self.hooks:
                h()

    def notify_core(self, status, addr=None, retry=3):
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

        # request = Req()
        # request.connect(zmqTCP('localhost', 10000))

        # ans = None
        msg = {'proc_info': (self.pid, self.name, status,)}
        # print(msg)

        # add a Sub() and get an ok from core???
        p = Pub()
        p.connect(zmqTCP('localhost', 9998), queue_size=1)
        for _ in range(retry):
            p.pub('core_info', msg)
            time.sleep(0.1)
        # return
        #
        # # this will block and wait for geckocore to respond
        # while not ans:
        #     ans = request.get(msg)
        #     # print("*** {} : {} ***".format(msg, ans))
        #     # time.sleep(0.01)
        #
        # # print("**** notify core:", ans)
        # request.close()
        # # time.sleep(5)


def init_node(**kwargs):
    """
    Initializes the node and sets up some global variables.
    """
    # this gets created inside a new process, so it should be ok
    global g_geckopy
    g_geckopy = GeckoPy(**kwargs)
    # print("M>> {}".format(g_geckopy))


def log(msg):
    """
    Prints a message to the log.
    """
    global g_geckopy
    if g_geckopy.queue:
        g_geckopy.queue.put((g_geckopy.pid, g_geckopy.name, msg,))
    else:
        print(Fore.BLUE + '{}[{}]:'.format(g_geckopy.name, g_geckopy.pid) + Fore.RESET + '{}'.format(msg))


def is_shutdown():
    """
    Returns true if it is time to shutdown.
    """
    global g_geckopy
    return g_geckopy.kill


# def Publisher(self, uds_file=None, host='localhost', queue_size=10, bind=False):
def Publisher(addr=None, queue_size=5, bind=False):
    """
    addr: either a valid tcp or uds address. If nothing is passed in, then
          it is set to what geckopy defaults to
    queue_size: how many messages to queue up, default is 5
    bind: by default this connects to geckocore, but you can also have it bind
          to a different port
    """
    global g_geckopy
    p = Pub()
    if addr is None:
        addr = g_geckopy.core_inaddr

    if bind:
        p.bind(addr, queue_size=queue_size)
    else:
        p.connect(addr, queue_size=queue_size)

    return p


# def Subscriber(self, topics, cb, host='localhost', uds_file=None):
def Subscriber(topics, cb_func, addr=None, bind=False):
    """
    addr: either a valid tcp or uds address. If nothing is passed in, then
          it is set to what geckopy defaults to
    queue_size: how many messages to queue up, default is 5
    bind: by default this connects to geckocore, but you can also have it bind
          to a different port
    """
    global g_geckopy
    s = Sub(cb_func=cb_func, topics=topics)
    if addr is None:
        addr = g_geckopy.core_outaddr

    if bind:
        s.bind(addr)
    else:
        s.connect(addr)

    g_geckopy.subs.append(s)


def on_shutdown(hook):
    """
    Allows you to setup hooks for when eveything shuts down. Function accepts
    no arguments.

    hook = function()

    This is an array, so functions are called in order they were put in:
    FIFO.
    """
    global g_geckopy
    g_geckopy.hooks.append(hook)


def spin(hertz=50):
    """
    This will continue to loop at the given hertz until is_shutdown() returns
    True.
    """
    global g_geckopy
    rate = Rate(hertz)
    while not g_geckopy.kill:
        for sub in g_geckopy.subs:
            sub.recv_nb()
        rate.sleep()
