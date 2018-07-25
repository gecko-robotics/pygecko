#!/usr/bin/env python3
from __future__ import print_function
import multiprocessing as mp
import time
import signal

def runable_process(ns, e, **kwargs):
    def signal_handler(signalnum, stackframe):
        print('ignore ctrl-c signal:', signalnum)
        # e.clear()
        # sys.exit(0)

    # kill -l
    # signal.signal(signal.SIGINT, signal_handler)
    # signal.signal(signal.SIGTERM, signal_handler)
    if kwargs.get('signal', False):
        signal.signal(signal.SIGINT, signal_handler)

    if kwargs:
        for k,v in kwargs.items():
            print('got: {} and {}'.format(k, v))

    ns.data = 1
    while e.is_set():
        ns.data += 1
        print("{}".format(ns.data))
        time.sleep(1)

if __name__ == "__main__":
    # from multiprocessing.managers import SyncManager
    # mgr = SyncManager(address=address, authkey=authkey)
    # mgr.start()
    mgr = mp.Manager()
    ns = mgr.Namespace()
    e = mp.Event()
    e.set()
    kw = {'a':1, 'b':2}
    runable_process(ns, e)
    # runable_process({'ns':1, 'e':e, 'bob':5})
