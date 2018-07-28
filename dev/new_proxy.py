#!/usr/bin/env python3

from __future__ import print_function

# fix path for now
import sys
sys.path.append("../")

from pygecko.transport import Pub, Sub
from pygecko.transport import zmqTCP
from pygecko.transport.core import GProcessProxy
import multiprocessing as mp
import os
import time


if __name__ == "__main__":
    gp = GProcessProxy()
    gp.start()

    print('Main process pid[{}]'.format(os.getpid()))
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("main loop got ctrl-c")

    gp.join(1)
