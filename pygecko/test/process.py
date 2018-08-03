from __future__ import print_function

import multiprocessing as mp
from pygecko.transport import zmqTCP
# import time
# import signal
# import os

class GeckoSimpleProcess(object):
    """
    A simple class to help processes start/stop easily
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
        kwargs = kwargs['kwargs']  # WTF???

        if 'core_inaddr' not in kwargs:
            kwargs['core_inaddr'] = in_addr = zmqTCP('localhost', 9998)  # FIXME: put in launch.json
        if 'core_outaddr' not in kwargs:
            kwargs['core_outaddr'] = in_addr = zmqTCP('localhost', 9999)  # FIXME: put in launch.json

        # print('ss', kwargs)

        self.ps = mp.Process(name=name, target=func, kwargs=kwargs)
        self.ps.start()
        print('>> Simple Process Started: {}[{}]'.format(self.ps.name, self.ps.pid))

    def join(self, timeout=None):
        print('>> Stopping {}[{}] ...'.format(self.ps.name, self.ps.pid), end=' ')
        if self.ps:
            self.ps.join(timeout)
            if self.ps.is_alive():
                self.ps.terminate()
        self.ps = None
        print('stopped')
