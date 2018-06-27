#!/usr/bin/env python

from __future__ import print_function
from pygecko.ZmqClass import Pub, Sub
from pygecko.ZmqClass import Core
import multiprocessing as mp
import time
import signal
import socket
import sys


def core(e):
    c = Core(('0.0.0.0', 9998), ('0.0.0.0', 9999))

def publisher(e):
    p = Pub()
    while e.is_set:
        p.pub('msg', 'hello')
        time.sleep(1)
    print('pub bye ...')

def subscriber(e):
    s = Sub(['msg'])
    while e.is_set:
        print(s.recv())
    print('sub bye ...')


if __name__ == '__main__':
    e = mp.Event()
    e.set()

    c = mp.Process(target=core, args=(e,), name='core')
    c.start()
    time.sleep(1)

    # p = mp.Process(target=publisher, args=(e,), name='publisher')
    # p.start()

    s = mp.Process(target=subscriber, args=(e,), name='subscriber')
    s.start()

    # def signal_handler(signalnum, stackframe):
    #     print('ctrl-c signal.')
    #     e.clear()
    #     sys.exit(0)
    #
    # # kill -l
    # signal.signal(signal.SIGINT, signal_handler)
    # signal.signal(signal.SIGTERM, signal_handler)

    while True:
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            print('ctrl-c')
        finally:
            e.clear()
            time.sleep(1)
            # p.join()
            s.join()
            c.join()
            break
