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
from colorama import Fore, Back, Style
from threading import Thread
from pygecko.transport.core import SignalCatch
from pygecko.transport.helpers import zmqTCP, zmqUDS
import psutil as psu
import time

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
