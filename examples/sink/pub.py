#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

from __future__ import print_function
# from pygecko.transport import zmqTCP
from pygecko.multiprocessing import geckopy
# from pygecko.test import GeckoSimpleProcess
from pygecko import Lidar
from random import randint
import time


def publisher(**kwargs):
    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(5)

    p = geckopy.Publisher()

    while not geckopy.is_shutdown():
        scan = []
        for a in range(360):
            r = 4000 + randint(0, 100)
            # scan.append((a, 5,))
            scan.append(r)  # 5m
        msg = Lidar(scan)
        p.pub('scan', msg)  # topic msg

        geckopy.log('[{}] published msg'.format(msg.timestamp))
        rate.sleep()
    print('pub bye ...')


if __name__ == '__main__':
    # normally you wouldn't run this here, but is running else where
    # this is just for testing
    # core = GeckoCore()
    # core.start()
    publisher()
