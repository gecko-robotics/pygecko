
from pygecko.transport.zmqclass import ZMQError
from pygecko.transport.zmqclass import Pub, Sub  #, SubNB
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
        # new_sleep = diff if diff < self.dt else 0
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

    def notify_core(self, status, addr=zmqTCP('localhost', 9998)):
        """
        this doen't work for some reason!!!!
        """
        print("********** wtf *************")

        # p = Pub()
        # p = self.Publisher(addr, queue_size=1)
        p = self.Publisher(addr)

        # p.connect(addr)
        for i in range(50):
            print("{},".format(i), end="")
            p.pub('core_info', (self.pid, self.name, status))
        time.sleep(0.001)
        print('')
        print("**** notify core:", status)
        time.sleep(5)

    # def Publisher(self, uds_file=None, host='localhost', queue_size=10, bind=False):
    def Publisher(self, addr=zmqTCP('localhost', 9998), queue_size=10, bind=False):

        p = Pub()

        # if uds_file:
        #     addr = zmqUDS(uds_file)
        # else:
        #     addr = zmqTCP(host, 9998)

        if bind:
            p.bind(addr, queue_size=queue_size)
        else:
            p.connect(addr, queue_size=queue_size)

        return p

    # def PublisherBind(self, uds_file=None, host='localhost', queue_size=10):
    #     """
    #     value?
    #     """
    #     p = Pub()
    #
    #     if uds_file:
    #         addr = zmqUDS(uds_file)
    #     else:
    #         addr = zmqTCP(host, 9998)
    #
    #     # p.connect(addr, queue_size=queue_size)
    #     p.bind(addr, queue_size=queue_size)
    #     return p

    # def Subscriber(self, topics, cb, host='localhost', uds_file=None):
    def Subscriber(self, topics, cb, addr=zmqTCP('localhost', 9999)):
        s = Sub(cb_func=cb, topics=topics)

        # if uds_file:
        #     addr = zmqUDS(uds_file)
        # else:
        #     addr = zmqTCP(host, 9999)

        s.connect(addr)
        self.subs.append(s)

    # def signal_handler(self, signalnum, stackframe):
    #     self.kill = True
    #     # print('ignore ctrl-c signal:', signalnum)
    #     # print('GeckoPy got ctrl-c:', signalnum)
    #     # print('kill =', self.kill)

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
        rate = self.Rate(1.2*hertz)
        while not self.kill:
            for sub in self.subs:
                sub.recv_nb()
            rate.sleep()
        if len(self.hooks) > 0:
            for h in self.hooks:
                h()
