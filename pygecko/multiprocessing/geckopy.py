##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################
# from pygecko.transport.zmq_base import ZMQError
from pygecko.transport.zmq_sub_pub import Pub, Sub
from pygecko.transport.srv import cService, cServiceProxy
from pygecko.transport.zmq_req_rep import Req
from pygecko.transport.helpers import zmqTCP
from pygecko.transport.helpers import GetIP
from pygecko.messages import Log
from pygecko.multiprocessing.sig import SignalCatch # capture signals in processes
from colorama import Fore, Style
import time
import os
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
        # geckopy info
        self.kill_signals()  # have to setup signals in new process
        self.subs = []   # subscriber nodes
        self.srvs = []   # services
        self.hooks = []  # functions to call on shutdown
        self.name = mp.current_process().name
        self.pid = mp.current_process().pid
        self.logpub = None

        # hard code for now
        if 'host' in kwargs.keys():
            host = kwargs.pop('host')
            if host == 'localhost':
                host = GetIP().get()
        else:
            host = GetIP().get()  # FIXME: kwargs should provide this
        self.req_addr = zmqTCP(host, 11311)  # set/get topic addrs
        self.proc_ip = host  # this ip address

    def __del__(self):
        if len(self.hooks) > 0:
            for h in self.hooks:
                h()

    def register_publisher(self, topics, port):
        addr = zmqTCP(self.proc_ip, port)
        msg = {
            'T': 0,  # publish
            'topics': topics,
            'addr': addr,
            'pid': self.pid,
            'name': self.name
        }

        request = Req()
        request.connect(self.req_addr)
        ans = request.get(msg)
        if ans is None or ans['status'] != 0:
            print("*** {} ***".format(ans))
            raise Exception("{}[{}]: Coundn't talk with core".format(self.name, self.pid))

        # request.close()

    def find_publisher(self, topic):
        msg = {
            'T': 1,  # subscriber
            'topics': topic,
            'pid': self.pid,
            'name': self.name
        }
        request = Req()
        request.connect(self.req_addr)
        ans = request.get(msg)
        if ans is None:
            raise Exception("{}[{}]: Coundn't talk with core".format(self.name, self.pid))

        # request.close()
        return ans

    def __format_print(self, topic, msg):
        # print(msg.level)
        # msg format: {proc_name, level, text}
        if msg.level == 'DEBUG': color = Fore.CYAN
        elif msg.level == 'WARN': color = Fore.YELLOW
        elif msg.level == 'ERROR': color = Fore.RED
        else: color = Fore.GREEN

        # shorten proc names??
        print(Style.BRIGHT + color + '>> {}:'.format(msg.name[:10]) + Style.RESET_ALL + msg.text)
        # print(">> {}: {}".format(topic, msg))

    def log(self, topic, msg):
        if self.logpub is None:
            self.__format_print(topic, msg)
        else:
            self.logpub.pub(topic, msg)


def init_node(**kwargs):
    """
    Initializes the node and sets up some global variables.
    """
    # this gets created inside a new process, so it should be ok
    global g_geckopy
    if g_geckopy is None:
        g_geckopy = GeckoPy(**kwargs)
        # print("Created geckopy >> {}".format(g_geckopy))


def loginfo(text, topic='log'):
    global g_geckopy
    msg = Log('INFO', g_geckopy.name, text)
    g_geckopy.log(topic, msg)


def logdebug(text, topic='log'):
    global g_geckopy
    msg = Log('DEBUG', g_geckopy.name, text)
    g_geckopy.log(topic, msg)


def logwarn(text, topic='log'):
    global g_geckopy
    msg = Log('WARN', g_geckopy.name, text)
    g_geckopy.log(topic, msg)


def logerror(text, topic='log'):
    global g_geckopy
    msg = Log('ERROR', g_geckopy.name, text)
    g_geckopy.log(topic, msg)


def is_shutdown():
    """
    Returns true if it is time to shutdown.
    """
    global g_geckopy
    return g_geckopy.kill


def Publisher(topics, addr=None, queue_size=5, bind=True):
    """
    addr: a valid tcp address: 1.1.1.1. If nothing is passed in, then
          it is set to what geckopy defaults to
    queue_size: how many messages to queue up, default is 5
    bind: by default this connects to geckocore, but you can also have it bind
          to a different port
    """
    global g_geckopy
    p = Pub()
    if (addr is None) and (bind):
        addr = g_geckopy.proc_ip
        addr = zmqTCP(addr)
        print('>> pub', addr)
        # addr = g_geckopy.core_inaddr

    if bind:
        port = p.bind(addr, queue_size=queue_size, random=True)
        g_geckopy.register_publisher(topics, port)
    else:
        p.connect(addr, queue_size=queue_size)

    return p


def Subscriber(topics, cb_func=None, addr=None, bind=False):
    """
    addr: either a valid tcp or uds address. If nothing is passed in, then
          it is set to what geckopy defaults to
    queue_size: how many messages to queue up, default is 5
    bind: by default this connects to geckocore, but you can also have it bind
          to a different port
    """
    global g_geckopy

    if len(topics) > 1:
        topics = [topics[0]]
        print("*** Sub topics can only be one, using:", topics)

    s = Sub(cb_func=cb_func, topics=topics)
    # if addr is None:
    #     addr = g_geckopy.core_outaddr

    if (addr is None) and (not bind):
        # addr = g_geckopy.proc_ip
        # addr = zmqTCP(addr)
        msg = g_geckopy.find_publisher(topics)
        if msg and msg['status'] != 0:
            raise Exception("Subscriber couldn't talk to core")
        else:
            addr = msg['addr']
        print('>> sub', addr)

    if bind:
        s.bind(addr)
    else:
        s.connect(addr)

    if cb_func:
        g_geckopy.subs.append(s)
    # should this be else: ???
    return s


# def Service(name, callback, addr):
#     """
#     name does nothing and i need to directly pass the address
#     """
#     global g_geckopy
#     s = cService(name, callback)
#     # bind or connect?
#     s.bind(addr)
#     # notify core??
#     # how do people find this?
#     g_gecko.srvs.append(s)


# def ServiceProxy(name, addr):
#     """
#     right now name does nothing and i need to pass an address
#
#     eventually name should be used in some manor to lookup the address
#     """
#     global g_geckopy
#     sp = cServiceProxy(name, addr)
#     # try:
#     #     sp = g_gecko.srvs[name]
#     # except KeyError:
#     #     logerror("ServiceProxy: {} not found".format(name))
#     #     sp = None
#     return sp


# def wait_for_service(name, timeout=None):
#     logerror("not sure wait_for_service is correct")
#     return True
#
#     global g_geckopy
#     # find service
#     # how???
#     start = time.time()
#     rate = Rate(10)
#     while name not in g_geckopy.srvs:
#         # ask core for service address?
#         # wait here for it ... how long?
#         rate.sleep()
#         if timeout:
#             if (start - time.time()) > timeout:
#                 return False
#     return True


# def on_shutdown(hook):
#     """
#     Allows you to setup hooks for when eveything shuts down. Function accepts
#     no arguments.
#
#     hook = function()
#
#     This is an array, so functions are called in order they were put in:
#     FIFO.
#     """
#     global g_geckopy
#     g_geckopy.hooks.append(hook)


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

        for srv in g_geckopy.srvs:
            srv.handle()

        rate.sleep()
