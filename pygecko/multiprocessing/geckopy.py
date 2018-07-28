
from pygecko.transport.zmqclass import ZMQError
from pygecko.transport.zmqclass import Pub, Sub, SubNB
from pygecko.transport.helpers import zmqTCP, zmqUDS
import signal
import time

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
        else:
            new_sleep = 0

        self.last_time = now

        time.sleep(new_sleep)


class GeckoPy(object):
    """
    This class setups a function in a new process. It also provides some useful
    functions for other things.
    """
    def __init__(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        self._kill = False
        self.subs = []   # subscriber nodes
        self.hooks = []  # functions to call on shutdown

    def is_shutdown(self):
        return self._kill

    def Rate(self, hertz):
        return GeckoRate(hertz)

    def get_time(self):
        return time.time()

    def Publisher(self, uds_file=None, host='localhost', queue_size=10):

        p = Pub()

        if uds_file:
            addr = zmqUDS(uds_file)
        else:
            addr = zmqTCP(host, 9998)

        p.connect(addr, queue_size=queue_size)
        # p.bind(addr, queue_size=queue_size)
        return p

    def PublisherBind(self, uds_file=None, host='localhost', queue_size=10):
        """
        value?
        """
        p = Pub()

        if uds_file:
            addr = zmqUDS(uds_file)
        else:
            addr = zmqTCP(host, 9998)

        # p.connect(addr, queue_size=queue_size)
        p.bind(addr, queue_size=queue_size)
        return p

    def Subscriber(self, topics, cb, host='localhost', uds_file=None):
        s = SubNB(cb, topics=topics)

        if uds_file:
            addr = zmqUDS(uds_file)
        else:
            addr = zmqTCP(host, 9999)

        s.connect(addr)
        self.subs.append(s)

    def signal_handler(self, signalnum, stackframe):
        self._kill = True
        # print('ignore ctrl-c signal:', signalnum)
        print('GeckoPy got ctrl-c:', signalnum)
        print('kill =', self._kill)

    def on_shutdown(self, hook):
        """
        Allows you to setup hooks for when eveything shuts down. Function accepts
        no arguments.

        hook = function()
        """
        self.hooks.append(hook)

    def spin(self, hertz=100):
        rate = self.Rate(1.2*hertz)
        while not self._kill:
            for sub in self.subs:
                sub.recv()
            rate.sleep()
        if len(self.hooks) > 0:
            for h in self.hooks:
                h()
