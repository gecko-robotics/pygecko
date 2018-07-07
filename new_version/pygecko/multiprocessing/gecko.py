##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import division, print_function
import multiprocessing as mp
from multiprocessing.managers import SyncManager


class GeckoProcess(object):
    """
    Base class that handles setup/teardown processes

    ['_Popen', '__class__', '__delattr__', '__dict__', '__doc__', '__format__',
    '__getattribute__', '__hash__', '__init__', '__module__', '__new__',
    '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__',
    '__str__', '__subclasshook__', '__weakref__', '_authkey', '_bootstrap',
    '_daemonic', '_identity', '_name', '_parent_pid', '_popen', '_tempdir',
    'authkey', 'daemon', 'exitcode', 'ident', 'is_alive', 'join', 'name', 'pid',
    'run', 'start', 'terminate']

    address=('127.0.0.1', 5000), authkey='abc'
    """
    def __init__(self, ps, address=('127.0.0.1', 8888), authkey='hi', to=1.0):
        print('CPU:', mp.cpu_count())

        self.ps = ps
        self.mgr = mp.Manager()
        # self.mgr = SyncManager(address=address, authkey=authkey)
        # self.mgr.start()
        self.namespace = self.mgr.Namespace()
        self.event = mp.Event()
        self.timeout = to

    def start(self):
        self.event.set()

        plist = []
        # for i, (mod, fun, args) in enumerate(ps['processes']):
        for (mod, fun, args) in self.ps['processes']:
            m = __import__(mod)
            ff = getattr(m, fun)
            if args is None:
                p = mp.Process(name=fun, target=ff, args=(self.namespace, self.event))
            else:
                p = mp.Process(name=fun, target=ff, args=(self.namespace, self.event, args))
            p.start()
            print('> Started:', mod + '.' + fun)
            plist.append(p)
        self.plist = plist

    def end(self):
        print('Main loop killing processes')
        # self.mgr.shutdown()
        for p in self.plist:
            p.join(timeout=self.timeout)
            if p.is_alive():
                print('had to kill a process:', p.name)
                p.terminate()
            else:
                print('clean exit:', p.name)
