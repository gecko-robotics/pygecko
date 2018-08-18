#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This really does a whole lot of nothing ... just launches some processes
# and passes some messages around. Make sure you run geckocore.py too.

from __future__ import print_function
import multiprocessing as mp
import time

try:
    import imutils
except ImportError as e:
    print(e)
    print('Please install imutils')
    exit(1)

# fix path for now
# once gecko is installed you don't need this kludge
# import sys
# sys.path.append("../../")

from pygecko.transport import Pub, Sub
from pygecko.transport import zmqTCP  #, GeckoCore
from pygecko.multiprocessing import geckopy
from math import sin, cos, pi, sqrt
import numpy as np

try:
    import cv2
except ImportError:
    # this works the cpu! only for testing when opencv not installed
    from pygecko.test import cv2


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


def pcv(**kwargs):
    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(10)

    topic = kwargs.get('topic', 'test')

    p = geckopy.Publisher()

    from imutils.video import WebcamVideoStream
    camera = WebcamVideoStream(src=0).start()

    datumn = time.time()

    while not geckopy.is_shutdown():
        img = camera.read()

        if img:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            shape = img.shape
            dtype = img.dtype
            img = img.tobytes()
            msg = {'img': img, 'shape': shape, 'dtype': dtype, 'stamp': time.time() - datumn}
            p.pub(topic, msg)  # topic msg
        else:
            print("*** couldn't read image ***")

        # sleep
        rate.sleep()

    # camera.release()
    camera.stop()
    print('cv bye ...')


def subscribe2(**kwargs):
    geckopy.init_node(**kwargs)

    def f(t, m):
        # print('>> Message[{}]'.format(t))
        if 'img' in m:
            im = m['img']
            im = np.frombuffer(im, dtype=m['dtype'])
            im = im.reshape(m['shape'])
            geckopy.log('image: {}x{}'.format(*im.shape[:2]))
        else:
            geckopy.log('msg: {}'.format(m))
            chew_up_cpu(.2)

    topic = kwargs.get('topic', 'test')
    s = geckopy.Subscriber([topic], f)  # array of topics to subscribe to
    geckopy.spin(20)


if __name__ == "__main__":
    # you can also run this file and it will run the function
    # alows modular development, don't have to run the whole gecko infrastructure
    # to test something ... but a lot may not happen though :)
    kw = {'topic': 'hello'}
    # publish(kwargs=kw)
    # pvc(kwargs=kw)
    subscribe2(kwargs=kw)
