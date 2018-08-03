#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import time

from pygecko.multiprocessing import GeckoPy


def movement(**kwargs):
    geckopy = GeckoPy(**kwargs)

    def f(t, m):
        geckopy.log('>> Message[{}]'.format(t))

    s = geckopy.Subscriber(['cmd', 'avoid'], f)
    geckopy.spin(20)


if __name__ == "__main__":
    kw = {}
    movement(kwargs=kw)
