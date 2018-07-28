from __future__ import print_function

import multiprocessing as mp
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
            self.join(1)

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
        self.ps = mp.Process(name=name, target=func, **kwargs)
        self.ps.start()
        print('>> Started: {}[{}]'.format(self.ps.name, self.ps.pid))

    def join(self, timeout=None):
        print('>> Stopping {}[{}] ...'.format(self.ps.name, self.ps.pid), end=' ')
        if self.ps:
            self.ps.join(timeout)
            if self.ps.is_alive():
                self.ps.terminate()
        self.ps = None
        print('stopped')
