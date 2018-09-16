#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################
# This really does a whole lot of nothing ... just launches some processes
# and passes some messages around. Make sure you run geckocore.py too.

import time
from pygecko.multiprocessing import geckopy
import numpy as np


def chew_up_cpu(interval):
    # chew up some cpu
    start = time.time()
    while (time.time() - start) < interval:
        5*5


def publish(**kwargs):
    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(1)

    topic = kwargs.get('topic', 'test')

    p = geckopy.Publisher()
    datumn = time.time()
    while not geckopy.is_shutdown():
        msg = {'time': time.time() - datumn, 'double': 3.14, 'int': 5, 'array': [1, 2, 3, 4, 5]}
        p.pub(topic, msg)

        # sleep
        rate.sleep()

    print('pub bye ...')


def subscribe2(**kwargs):
    geckopy.init_node(**kwargs)

    def f(t, m):
        # print('>> Message[{}]'.format(t))
        if 'img' in m:
            im = m['img']
            im = np.frombuffer(im, dtype=m['dtype'])
            im = im.reshape(m['shape'])
            geckopy.loginfo('image: {}x{}'.format(*im.shape[:2]))
        else:
            geckopy.logwarn('msg: {}'.format(m))
            chew_up_cpu(.2)

    topic = kwargs.get('topic', 'test')
    geckopy.Subscriber([topic], f)  # array of topics to subscribe to
    geckopy.spin(20)


if __name__ == "__main__":
    # you can also run this file and it will run the function
    # alows modular development, don't have to run the whole gecko infrastructure
    # to test something ... but a lot may not happen though :)
    kw = {'topic': 'hello'}
    # publish(kwargs=kw)
    subscribe2(kwargs=kw)
