#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################
#
from pygecko.multiprocessing import geckopy
from pygecko import Lidar
from random import randint


def publisher(**kwargs):
    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(5)

    p = geckopy.Publisher()

    while not geckopy.is_shutdown():
        scan = []
        for angle in range(360):
            r = 4000 + randint(0, 100)
            scan.append((angle, r,))  # 5m
        msg = Lidar(scan)
        p.pub('scan', msg)  # topic msg

        geckopy.log('[{}] published msg'.format(msg.timestamp))
        rate.sleep()
    print('pub bye ...')


if __name__ == '__main__':
    # you need to already have a geckocore running
    publisher()
