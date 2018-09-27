##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import division, print_function, absolute_import
import multiprocessing as mp
import os
import sys
import platform
# from pygecko.multiprocessing.sig import SignalCatch
# from pygecko.transport.helpers import zmqTCP, zmqUDS
# from pygecko.transport.beacon import BeaconFinder
# from pygecko.transport.beacon import get_host_key
# from pygecko.multiprocessing.corefinder import CoreFinder
from pygecko.multiprocessing.process import GeckoSimpleProcess
# from pygecko.transport import GeckoCore
import time


class GeckoLauncher(object):
    """
    Base class that handles setup/teardown processes

    Don't like name, maybe

    GeckoEngine
    GeckoManager
    GeckoLoop
    GeckoMultiprocessing -> gmp

    ['_Popen', '__class__', '__delattr__', '__dict__', '__doc__', '__format__',
    '__getattribute__', '__hash__', '__init__', '__module__', '__new__',
    '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__',
    '__str__', '__subclasshook__', '__weakref__', '_authkey', '_bootstrap',
    '_daemonic', '_identity', '_name', '_parent_pid', '_popen', '_tempdir',
    'authkey', 'daemon', 'exitcode', 'ident', 'is_alive', 'join', 'name', 'pid',
    'run', 'start', 'terminate']

    address=('127.0.0.1', 5000), authkey='abc'
    """
    plist = []
    core = None

    def __init__(self, ps, to=1.0):
        print('+', '-'*40, sep='')
        print('| geckolaunch')
        print('+', '-'*40, sep='')
        print('| Python: {}.{}.{}'.format(*tuple(platform.sys.version_info)[:3]))
        print('| OS: {}'.format(platform.system()))
        print('| CPU:', mp.cpu_count())
        print('| Processes: {}'.format(len(ps['processes'])))
        print('+', '-'*40, sep='')
        print('')

        self.ps = ps
        self.timeout = to

    def launch(self):
        """
        have process ignore ctrl-c (sigint) by setting kwargs['signal'] = True

        For macOs:
        kevin@Dalek processes $ kill -l
         1) SIGHUP      2) SIGINT      3) SIGQUIT     4) SIGILL
         5) SIGTRAP     6) SIGABRT     7) SIGEMT      8) SIGFPE
         9) SIGKILL    10) SIGBUS     11) SIGSEGV    12) SIGSYS
        13) SIGPIPE    14) SIGALRM    15) SIGTERM    16) SIGURG
        17) SIGSTOP    18) SIGTSTP    19) SIGCONT    20) SIGCHLD
        21) SIGTTIN    22) SIGTTOU    23) SIGIO      24) SIGXCPU
        25) SIGXFSZ    26) SIGVTALRM  27) SIGPROF    28) SIGWINCH
        29) SIGINFO    30) SIGUSR1    31) SIGUSR2
        """

        # list of process to shutdown when done
        plist = self.plist

        # find the core
        # finder = CoreFinder(self.pid, self.name, **kwargs)
        # in_addr = finder.core_inaddr
        # out_addr = finder.core_outaddr

        # save some stuff
        args = {}
        # args['python'] = tuple(platform.sys.version_info)[:3]
        args['os'] = platform.system()

        if 'geckocore' in self.ps:
            args['geckocore'] = self.ps['geckocore']
        else:
            raise Exception("GeckoLauncher: launch file needs to have geckocore section")

        # if 'start_core' in self.ps:
        #     # start core here
        #     # pass
        #     if self.ps['start_core']:
        #         self.core = GeckoCore()
        #         self.core.start()

        sys.path.append(os.getcwd())  # put module directory in path
        for cmd in self.ps['processes']:
            # tuple of inputs:
            #   mod: is the file to look in
            #   fun: is the function in the file to call
            #   args: are arguments to the function
            if len(cmd) == 2:
                (mod, fun) = cmd
                args = {}
            elif len(cmd) == 3:
                (mod, fun, args) = cmd
            else:
                raise Exception("** GeckoProcess Error: Wrong number of args for process **")

            # load the module and get the function
            m = __import__(mod)
            ff = getattr(m, fun)

            # start a process
            p = GeckoSimpleProcess()
            p.start(func=ff, name=fun, kwargs=args)

            print('>> Started:', mod + '.' + fun)
            plist.append(p)

        # save for when we have to shut all of this down
        self.plist = plist

    def __del__(self):
        if len(self.plist) > 0:
            self.end()

    def end(self):
        print('Main loop killing processes')
        self.plist = []

    def loop(self):

        self.launch()

        try:
            while True:
                time.sleep(1)

        except (KeyboardInterrupt, SystemExit):
            time.sleep(0.1)

        finally:
            self.end()





# http://jtushman.github.io/blog/2014/01/14/python-%7C-multiprocessing-and-interrupts/
# from multiprocessing import Process
# from multiprocessing.managers import SyncManager
# import signal
# from time import sleep
#
# # initializer for SyncManager
# def mgr_init():
#     signal.signal(signal.SIGINT, signal.SIG_IGN)
#     print 'initialized manager'
#
# def f(process_number, shared_array):
#     try:
#         print "starting thread: ", process_number
#         while True:
#             shared_array.append(process_number)
#             sleep(3)
#     except KeyboardInterrupt:
#         print "Keyboard interrupt in process: ", process_number
#     finally:
#         print "cleaning up thread", process_number
#
# if __name__ == '__main__':
#
#     processes = []
#
#   # now using SyncManager vs a Manager
#     manager = SyncManager()
#     # explicitly starting the manager, and telling it to ignore the interrupt signal
#     manager.start(mgr_init)
#     try:
#         shared_array = manager.list()
#
#         for i in xrange(4):
#             p = Process(target=f, args=(i, shared_array))
#             p.start()
#             processes.append(p)
#
#         try:
#             for process in processes:
#                 process.join()
#         except KeyboardInterrupt:
#             print "Keyboard interrupt in main"
#
#         for item in shared_array:
#             # we still have access to it!  Yay!
#             print item
#     finally:
#       # to be safe -- explicitly shutting down the manager
#         manager.shutdown()
