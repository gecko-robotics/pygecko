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
# import logging
# import logging.config
# import logging.handlers
from colorama import Fore, Back, Style
from threading import Thread
from pygecko.transport.core import SignalCatch
from pygecko.transport.helpers import zmqTCP, zmqUDS
import psutil as psu
import time
# from pprint import pprint  # doesnt  work with colorama!


class GeckoLog(SignalCatch):
    """
    This captures all log messages and prints them out. It will run until the
    multiprocessing.Event is cleared. Messages are passed to it via a
    multiprocessing.Queue. Colors are automatically assigned and if you need
    to change the colors because of terminal color, just change the values
    in the array self.color:

    self.colors = [Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]

    Message format: tuple(pid, process_name, string_to_print,)

    Right now, messages are passed via one que
    """
    def __init__(self):
        # self.colors = [Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
        self.colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
        self.index = 0
        self.pid_colors = {}

    def run(self, e, q):
        """
        e: multiprocessing.Event tells GeckoLog when to shutdown
        q: multiprocessing.Queue which is filled from GeckoPy.log() and printed
           out here
        """
        self.kill_signals()  # have to setup signals in new process
        while e.is_set():
            # see if anything is in the queue, non-blocking so it will be able
            # to handle the kill signal
            try:
                pid, name, msg = q.get(timeout=0.1) # wait for message
            except:
                pid = None

            # if we got something above, then print it out
            # if this is the first time this pid has been seen, add it to the
            # list of known pids/colors and print out the message
            if pid:
                try:
                    color = self.pid_colors[pid]
                except KeyError:
                    self.pid_colors[pid] = self.colors[self.index]
                    self.index = (self.index + 1) % len(self.colors)
                    color = self.pid_colors[pid]

                print(Style.BRIGHT + Back.WHITE + color + '{}[{}]:'.format(name, pid) + Style.RESET_ALL + msg)


class GeckoFactory(object):
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
        self.event = mp.Event()
        self.timeout = to

    def start_logger(self):
        # setup logging
        self.gecko_log = GeckoLog()
        self.queue = mp.Queue()
        self.t = mp.Process(target=self.gecko_log.run, name="GeckoLog", args=(self.event, self.queue,))
        # self.t.daemon = True
        self.t.start()

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
        self.event.set()

        self.start_logger()

        # # setup logging
        # self.gecko_log = GeckoLog()
        # self.queue = mp.Queue()
        # self.t = mp.Process(target=self.gecko_log.run, name="GeckoLog", args=(self.event, self.queue,))
        # # self.t.daemon = True
        # self.t.start()

        # list of process to shutdown when done
        plist = []

        # get GeckoCore addresses, either TCP or UDS
        if 'geckocore' in self.ps:
            kind = self.ps['geckocore']['type']
            if kind == 'tcp':
                h, p = self.ps['geckocore']['in']
                in_addr = zmqTCP(h, p)
                h, p = self.ps['geckocore']['out']
                out_addr = zmqTCP(h, p)
            elif kind == 'uds':
                f = self.ps['geckocore']['in']
                in_addr = zmqUDS(f)
                f = self.ps['geckocore']['out']
                out_addr = zmqUDS(f)
                # raise NotImplementedError(kind)
        else:
            in_addr = zmqTCP('localhost', 9998)
            out_addr = zmqTCP('localhost', 9999)

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

            # save some stuff
            args['pyton'] = tuple(platform.sys.version_info)[:3]
            args['os'] = platform.system()
            args['queue'] = self.queue  # pass log queue
            args['core_inaddr'] = in_addr
            args['core_outaddr'] = out_addr

            # load the module and get the function
            m = __import__(mod)
            ff = getattr(m, fun)

            p = mp.Process(name=fun, target=ff, kwargs=args)

            p.start()
            print('>> Started:', mod + '.' + fun)
            plist.append(p)

        # save for when we have to shut all of this down
        self.plist = plist

    def __del__(self):
        # kill the logger
        self.event.clear()
        self.t.join(timeout=0.1)
        if self.t.is_alive():
            self.t.terminate()

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


class GeckoLauncher(GeckoFactory):
    def __init__(self, ps):
        GeckoProcess.__init__(self, ps)

    def loop(self):

        self.launch()

        try:
            # alive = mp.active_children()
            # palive = [psu.Process(p.pid) for p in alive]

            while self.event.is_set():
                time.sleep(1)
                # print('+', '-'*30, sep='')
                # print('| Alive processes:', len(alive))
                # print('+', '-'*30, sep='')
                # for ps, p in zip(palive, alive):
                #     pd = ps.as_dict(attrs=['connections','cpu_percent','memory_percent'])
                #     label = '{}[{}]'.format(p.name, p.pid)
                #     print('| {:.<30} cpu: {:5}%    mem: {:6.2f}%'.format(label, pd['cpu_percent'], pd['memory_percent']))

        except (KeyboardInterrupt, SystemExit) as e:
            if KeyboardInterrupt == type(e):
                err = 'ctrl-C'
            elif SystemExit == type(e):
                err = 'exit'
            # print('\n>> Received {}\n'.format(err))

            # set the kill flag
            self.event.clear()
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
