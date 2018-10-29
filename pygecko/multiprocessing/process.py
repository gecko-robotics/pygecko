##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################
from __future__ import print_function
import multiprocessing as mp
from pygecko.transport.helpers import zmqTCP


class GeckoSimpleProcess(object):
    """
    A simple class to help processes start/stop easily. It is main intended for
    testing and some simple things.

    p = GeckoSimpleProcess()  # create process
    p.start(function)         # start the process, runs function
    ...                       # stuff happens
    p.join()                  # time to go ... bye!
    """
    ps = None

    def __del__(self):
        if self.ps:
            self.join(0.1)

    @property
    def name(self):
        return self.ps.name

    @property
    def pid(self):
        return self.ps.pid

    def is_alive(self):
        if self.ps:
            return self.ps.is_alive()
        else:
            return False

    def terminate(self):
        if self.ps:
            self.ps.terminate()

    def start(self, func, name='simple_process', **kwargs):
        if kwargs:
            kwargs = kwargs['kwargs']  # WTF???
        else:
            kwargs = {"host": "localhost"}

        # if 'core_inaddr' not in kwargs:
        #     kwargs['core_inaddr'] = zmqTCP('localhost', 9998)  # FIXME: put in launch.json
        # if 'core_outaddr' not in kwargs:
        #     kwargs['core_outaddr'] = zmqTCP('localhost', 9999)  # FIXME: put in launch.json

        self.ps = mp.Process(name=name, target=func, kwargs=kwargs)
        self.ps.start()
        print('>> Simple Process Started: {}[{}]'.format(self.ps.name, self.ps.pid))

    def join(self, timeout=None):
        print('>> Stopping Simple Process {}[{}] ...'.format(self.ps.name, self.ps.pid), end=' ')
        if self.ps:
            self.ps.join(timeout)
            if self.ps.is_alive():
                self.ps.terminate()
        self.ps = None
        # print('stopped')
