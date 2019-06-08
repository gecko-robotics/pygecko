##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################
# from pygecko.transport.zmq_base import ZMQError
from pygecko.transport.zmq_sub_pub import Pub, Sub
# from pygecko.transport.srv import cService, cServiceProxy
# from pygecko.transport.zmq_req_rep import Req
from pygecko.transport.helpers import zmqTCP
from pygecko.transport.helpers import zmqUDS
from pygecko.transport.helpers import GetIP
# from pygecko.gecko_enums import Status
# from pygecko.gecko_enums import ZmqType
from pygecko.messages import Log
from pygecko.multiprocessing.sig import SignalCatch  # capture signals in processes
from colorama import Fore, Style
import time
# import os
import multiprocessing as mp

from pygecko.transport.beacon import BeaconFinder

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
        # self.subs = []   # subscriber nodes
        # self.srvs = []   # services
        # self.hooks = []  # functions to call on shutdown
        self.name = mp.current_process().name
        self.pid = mp.current_process().pid
        self.logpub = None

        # hard code for now
        # if 'host' in kwargs.keys():
        #     host = kwargs.pop('host')
        #     if host == 'localhost':
        #         host = GetIP().get()
        # else:
        host = GetIP().get()  # FIXME: kwargs should provide this
        # self.req_addr = zmqTCP(host, 11311)  # set/get topic addrs
        self.proc_ip = host  # this ip address

        print("----------------------------------")
        print("GeckoPy")
        print("-----------")
        print("  Process:", self.name)
        print("  PID:", self.pid)
        print("  Host: {}".format(self.proc_ip))
        print("----------------------------------")

    # def __del__(self):
    #     if len(self.hooks) > 0:
    #         for h in self.hooks:
    #             h()

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
            self.logpub.publish(msg)


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


def shutdown():
    print("*** geckopy::shutdown: not implemented now ***")
    # global g_geckopy
    # g_geckopy.kill = True


def ok():
    """
    Returns true if it is time to shutdown.
    """
    global g_geckopy
    return not g_geckopy.kill


def Binder(key, topic, Conn, fname=None, queue_size=5):
    """
    Creates a publisher that can either connect or bind to an address.

    bind -> (key, topic, pid, endpt)
    bind <- (key, topic, pid, ok)

    key: geckocore key
    topic: pub/sub topic name
    Conn: either Pub or Sub
    fname: file path for UDS
    queue_size: how many messages to queue up, default is 5
    """
    global g_geckopy
    p = Conn()
    p.topics = topic  # need to keep track
    # if (addr is None) and (bind):
    # addr = g_geckopy.proc_ip
    # addr = Proto(addr)
    # print('>> pub', addr)
    # addr = g_geckopy.core_inaddr

    # if bind:
    # port = p.bind(addr, queue_size=queue_size, random=True)
    # g_geckopy.register_publisher(topics, port)
    bf = BeaconFinder(key)
    pid = mp.current_process().pid

    if fname:
        addr = zmqUDS(fname)
        p.bind(addr, queue_size=queue_size)
        msg = (key, topic, str(pid), addr)

        # print(p)
        # print(msg)
    else:
        addr = g_geckopy.proc_ip
        addr = zmqTCP(addr)
        port = p.bind(addr, queue_size=queue_size, random=True)
        msg = (key, topic, str(pid), zmqTCP(g_geckopy.proc_ip, port))

    retry = 5

    for _ in range(retry):
        data = bf.send(msg)
        print(data)

        if data is None:
            time.sleep(0.5)
            continue

        if (len(data) == 4) and (data[0] == key) and (data[1] == topic) and (data[3] == "ok"):
            return p
    return None


def pubBinderTCP(key, topic, queue_size=5):
    return Binder(key, topic, Pub, queue_size=queue_size)


def pubBinderUDS(key, topic, fname, queue_size=5):
    return Binder(key, topic, Pub, fname=fname, queue_size=queue_size)


def subBinderTCP(key, topic, queue_size=5):
    return Binder(key, topic, Sub, queue_size=queue_size)


def subBinderUDS(key, topic, fname, queue_size=5):
    return Binder(key, topic, Sub, fname=fname, queue_size=queue_size)


def Connector(key, topic, Proto, queue_size=5):
    """
    Creates a publisher that can either connect or bind to an address.

    conn -> (key, topic, pid)
    conn <- (key, topic, endpt)
    conn <- (key, topic, pid, endpt)

    key: geckocore key
    topic: pub/sub topic name
    Proto: either Pub or Sub
    queue_size: how many messages to queue up, default is 5
    """
    global g_geckopy

    bf = BeaconFinder(key)
    pid = mp.current_process().pid
    msg = (key, topic, str(pid))
    retry = 5
    data = None

    for _ in range(retry):
        data = bf.send(msg)
        print(data)

        if data is None:
            time.sleep(0.5)
            continue

        if (len(data) == 3) and (data[0] == key) and (data[1] == topic):
            p = Proto()
            p.connect(data[2])
            return p

    return None


def pubConnectTCP(key, topic, queue_size=5):
    return Connector(key, topic, Pub, queue_size)


def pubConnectUDS(key, topic, queue_size=5):
    return Connector(key, topic, Pub, queue_size)


def subConnectTCP(key, topic, queue_size=5):
    return Connector(key, topic, Sub, queue_size)


def subConnectUDS(key, topic, queue_size=5):
    return Connector(key, topic, Sub, queue_size)

    # """
    # Creates a publisher that can either connect or bind to an address.
    #
    # addr: a valid tcp address: 1.1.1.1. If nothing is passed in, then
    #       it is set to what geckopy defaults to
    # queue_size: how many messages to queue up, default is 5
    # bind: by default this connects to geckocore, but you can also have it bind
    #       to a different port
    # """
    # global g_geckopy
    #
    # bf = BeaconFinder(key)
    # pid = mp.current_process().pid
    # msg = (key, topic, str(pid))
    # retry = 5
    # data = None
    #
    # for _ in range(retry):
    #     data = bf.send(msg)
    #     print(data)
    #
    #     if data is None:
    #         time.sleep(0.5)
    #         continue
    #
    #     if (len(data) == 3) and (data[0] == key) and (data[1] == topic):
    #         s = Sub()
    #         s.connect(data[2])
    #         return s
    #
    # return None


# def subConnectUDS(key, topic, queue_size=5):
#     return Connector(key, topic, Sub, queue_size)
    # """
    # Creates a publisher that can either connect or bind to an address.
    #
    # addr: a valid tcp address: 1.1.1.1. If nothing is passed in, then
    #       it is set to what geckopy defaults to
    # queue_size: how many messages to queue up, default is 5
    # bind: by default this connects to geckocore, but you can also have it bind
    #       to a different port
    # """
    # global g_geckopy
    #
    # bf = BeaconFinder(key)
    # pid = mp.current_process().pid
    # msg = (key, topic, str(pid))
    # retry = 5
    # data = None
    #
    # for _ in range(retry):
    #     data = bf.send(msg)
    #     print(data)
    #
    #     if data is None:
    #         time.sleep(0.5)
    #         continue
    #
    #     if (len(data) == 3) and (data[0] == key) and (data[1] == topic):
    #         s = Sub()
    #         s.connect(data[2])
    #         return s
    #
    # return None


# def spin(hertz=50):
#     """
#     This will continue to loop at the given hertz until is_shutdown() returns
#     True.
#     """
#     global g_geckopy
#     rate = Rate(hertz)
#     while not g_geckopy.kill:
#         for sub in g_geckopy.subs:
#             sub.recv_nb()
#
#         for srv in g_geckopy.srvs:
#             srv.handle()
#
#         rate.sleep()

###########################################################################
# def Subscriber(topics, cb_func=None, addr=None, bind=False):
#     """
#     Creates a subscriber that can connect or bind to an address.
#
#     addr: either a valid tcp or uds address. If nothing is passed in, then
#           it is set to what geckopy defaults to
#     queue_size: how many messages to queue up, default is 5
#     bind: by default this connects to geckocore, but you can also have it bind
#           to a different port
#     """
#     global g_geckopy
#
#     if len(topics) > 1:
#         topics = [topics[0]]
#         print("*** Sub topics can only be one, using:", topics)
#
#     s = Sub(cb_func=cb_func, topics=topics)
#     # if addr is None:
#     #     addr = g_geckopy.core_outaddr
#
#     if (addr is None) and (not bind):
#         # addr = g_geckopy.proc_ip
#         # addr = zmqTCP(addr)
#         msg = g_geckopy.find_publisher(topics)
#         if msg and msg['status'] != Status.ok:
#             raise Exception("Subscriber couldn't talk to core")
#         else:
#             addr = msg['addr']
#         print('>> sub', addr)
#
#     if bind:
#         s.bind(addr)
#     else:
#         s.connect(addr)
#
#     if cb_func:
#         g_geckopy.subs.append(s)
#     # should this be else: ???
#     return s

# def Publisher(topics, addr=None, queue_size=5, bind=True):
#     """
#     Creates a publisher that can either connect or bind to an address.
#
#     addr: a valid tcp address: 1.1.1.1. If nothing is passed in, then
#           it is set to what geckopy defaults to
#     queue_size: how many messages to queue up, default is 5
#     bind: by default this connects to geckocore, but you can also have it bind
#           to a different port
#     """
#     global g_geckopy
#     p = Pub()
#     p.topics = topics  # need to keep track
#     if (addr is None) and (bind):
#         addr = g_geckopy.proc_ip
#         addr = zmqTCP(addr)
#         # print('>> pub', addr)
#         # addr = g_geckopy.core_inaddr
#
#     if bind:
#         port = p.bind(addr, queue_size=queue_size, random=True)
#         g_geckopy.register_publisher(topics, port)
#     else:
#         p.connect(addr, queue_size=queue_size)
#
#     return p

# def SubscriberMulti(topics, cb_func=None, addr=None, bind=False):
#     """
#     Creates a subscriber that can connect or bind to an address.
#
#     addr: either a valid tcp or uds address. If nothing is passed in, then
#           it is set to what geckopy defaults to
#     queue_size: how many messages to queue up, default is 5
#     bind: by default this connects to geckocore, but you can also have it bind
#           to a different port
#     """
#     global g_geckopy
#
#     # if len(topics) > 1:
#     #     topics = [topics[0]]
#     #     print("*** Sub topics can only be one, using:", topics)
#
#     s = Sub(cb_func=cb_func, topics=topics)
#
#     if (addr is None) and (not bind):
#         # addr = g_geckopy.proc_ip
#         # addr = zmqTCP(addr)
#         msg = g_geckopy.find_publisher(topics)
#         if msg and msg['status'] != Status.ok:
#             raise Exception("Subscriber couldn't talk to core")
#         else:
#             addr = msg['addr']
#         print('>> sub', addr)
#
#     if bind:
#         s.bind(addr)
#     else:
#         s.connect(addr)
#
#     if cb_func:
#         g_geckopy.subs.append(s)
#     # should this be else: ???
#     return s

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

# def register_publisher(self, topics, port):
#     addr = zmqTCP(self.proc_ip, port)
#     msg = {
#         'T': ZmqType.pub,  # publish
#         'topics': topics,
#         'addr': addr,
#         'pid': self.pid,
#         'name': self.name
#     }
#
#     request = Req()
#     request.connect(self.req_addr)
#     ans = request.get(msg)
#     if ans is None or ans['status'] != Status.ok:
#         print("*** {} ***".format(ans))
#         raise Exception("{}[{}]: Coundn't talk with core".format(self.name, self.pid))

    # request.close()
# def find_publisher2(self, topics):
#     ret = {}
#
#     request = Req()
#     request.connect(self.req_addr)
#
#     for topic in topics:
#         msg = {
#             'T': ZmqType.sub,  # subscriber
#             'topics': topic,
#             'pid': self.pid,
#             'name': self.name
#         }
#         ans = request.get(msg)
#         if ans:
#             if ans['status'] == Status.ok:
#                 try:
#                     ret[ans['addr']].append(ans['topic'])
#                 except:
#                     ret[ans['addr']] = [ans['topic']]
#
#     # request.close()
#     return ans

# def find_publisher(self, topics):
#     msg = {
#         'T': ZmqType.sub,  # subscriber
#         'topics': topics,
#         'pid': self.pid,
#         'name': self.name
#     }
#     request = Req()
#     request.connect(self.req_addr)
#     ans = None
#     for i in range(5):
#         ans = request.get(msg)
#         if ans is None:
#             # raise Exception("{}[{}]: Coundn't talk with core".format(self.name, self.pid))
#             ans = {'status': Staus.core_not_found}
#         else:
#             break
#
#     # request.close()
#     return ans
