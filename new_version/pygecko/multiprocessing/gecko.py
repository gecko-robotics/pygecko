##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import division, print_function
import multiprocessing as mp
from multiprocessing.managers import SyncManager
import platform
import logging
import logging.config
import logging.handlers

"""
kevin@Dalek ~ $ pstree -s python
-+= 00001 root /sbin/launchd
 |-+= 00309 kevin /Applications/Utilities/Terminal.app/Contents/MacOS/Terminal -psn_0_61455
 | \-+= 05608 root login -pfl kevin /bin/bash -c exec -la bash /bin/bash
 |   \-+= 05609 kevin -bash
 |     \-+= 10323 kevin /usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/Resources/Python.app/Co
 |       |--- 10326 kevin /usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/Resources/Python.app/
 |       |--- 10327 kevin /usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/Resources/Python.app/
 |       |--- 10328 kevin /usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/Resources/Python.app/
 |       \--- 10329 kevin /usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/Resources/Python.app/
 |-+= 00491 kevin /Applications/Dropbox.app/Contents/MacOS/Dropbox
 | \--- 00496 kevin /Applications/Dropbox.app/Contents/MacOS/Dropbox -type:exit-monitor -python-version:2.7.11 -method:
 \--- 00495 kevin /Applications/Dropbox.app/Contents/MacOS/Dropbox -type:crashpad-handler --capture-python --no-upload-
"""


class GeckoProcess(object):
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
    def __init__(self, ps, address=('127.0.0.1', 8888), authkey='hi', to=1.0):
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
        self.mgr = mp.Manager()
        # self.mgr = SyncManager(address=address, authkey=authkey)
        # self.mgr.start()
        self.namespace = self.mgr.Namespace()
        self.event = mp.Event()
        self.timeout = to

    def start(self):
        """
        have process ignore ctrl-c (sigint) by setting kwargs['signal'] = True

        kevin@Dalek processes $ kill -l
         1) SIGHUP	 2) SIGINT	 3) SIGQUIT	 4) SIGILL
         5) SIGTRAP	 6) SIGABRT	 7) SIGEMT	 8) SIGFPE
         9) SIGKILL	10) SIGBUS	11) SIGSEGV	12) SIGSYS
        13) SIGPIPE	14) SIGALRM	15) SIGTERM	16) SIGURG
        17) SIGSTOP	18) SIGTSTP	19) SIGCONT	20) SIGCHLD
        21) SIGTTIN	22) SIGTTOU	23) SIGIO	24) SIGXCPU
        25) SIGXFSZ	26) SIGVTALRM	27) SIGPROF	28) SIGWINCH
        29) SIGINFO	30) SIGUSR1	31) SIGUSR2
        """
        self.event.set()

        plist = []
        # for i, (mod, fun, args) in enumerate(ps['processes']):
        for cmd in self.ps['processes']:
            if len(cmd) == 2:
                (mod, fun) = cmd
                args = {'signal': True}
            elif len(cmd) == 3:
                (mod, fun, args) = cmd
                args['signal'] = True
            else:
                raise Exception("** GeckoProcess Error: Wrong number of args for process **")

            # load the module and get the function
            m = __import__(mod)
            ff = getattr(m, fun)

            # if args is None:
            #     p = mp.Process(name=fun, target=ff, args=(self.namespace, self.event,))
            # else:
            #     p = mp.Process(name=fun, target=ff, args=(self.namespace, self.event,), kwargs=args)
            p = mp.Process(name=fun, target=ff, args=(self.namespace, self.event), kwargs=args)

            p.start()
            print('>> Started:', mod + '.' + fun)
            plist.append(p)
        self.plist = plist

    def __del__(self):
        if len(self.plist) > 0:
            self.end()

    def end(self):
        print('Main loop killing processes')
        # self.mgr.shutdown()
        for p in self.plist:
            p.join(timeout=self.timeout)
            if p.is_alive():
                print('** Had to terminate() process:', p.name)
                p.terminate()
            else:
                print('>> Clean exit:', p.name)
        self.plist = []

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
