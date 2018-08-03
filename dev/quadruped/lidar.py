#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import time
from pygecko.multiprocessing import GeckoPy

def bye():
    print('='*40)
    print(' lidar bye ...')
    print('='*40)


def lidar(**kwargs):
    geckopy = GeckoPy(**kwargs)
    rate = geckopy.Rate(1)

    p = geckopy.Publisher()

    while not geckopy.is_shutdown():
        msg = "hi"

        p.pub('avoid', msg)

        # sleep
        rate.sleep()


if __name__ == "__main__":
    kw = {}
    lidar(kwargs=kw)
