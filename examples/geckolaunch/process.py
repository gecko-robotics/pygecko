#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import multiprocessing as mp
import time
import signal

# fix path for now
# once gecko is installed you don't need this kludge
import sys
sys.path.append("../../")

from pygecko.transport import Pub, Sub
from pygecko.transport.zmqclass import SubNB
from pygecko.transport import zmqTCP, GeckoCore
from pygecko.multiprocessing import GeckoPy
from math import sin, cos, pi, sqrt

try:
    import cv2
except ImportError:
    # this works the cpu! only for testing when opencv not installed
    from pygecko.test import cv2


def chew_up_cpu():
    # chew up some cpu
    for i in range(90):
        m = sin(i*pi/180)*cos(i*pi/180)*sin(i*pi/180)*cos(i*pi/180)*sin(i*pi/180)*cos(i*pi/180)
        sqrt(m**9)


def publish(**kwargs):
    geckopy = GeckoPy()
    rate = geckopy.Rate(20)

    topic = kwargs.get('topic', 'test')

    p = geckopy.Publisher()

    while not geckopy.is_shutdown():
        msg = {'time': time.time(), 'double': 3.14, 'int': 5, 'array': [1, 2, 3, 4, 5]}
        p.pub(topic, msg)
        # print('>> published msg on topic {}'.format(topic))

        # chew up some cpu
        # chew_up_cpu()

        # sleep
        rate.sleep()

    print('pub bye ...')


def pcv(**kwargs):
    geckopy = GeckoPy()
    rate = geckopy.Rate(30)

    topic = kwargs.get('topic', 'test')

    p = geckopy.Publisher()

    camera = cv2.VideoCapture(0)
    camera.set(3, 640)
    camera.set(4, 480)

    while not geckopy.is_shutdown():
        ok, img = camera.read()
        if ok:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = img.tobytes()
            msg = {'img': img, 's': time.time()}
            p.pub(topic, msg)  # topic msg

        # sleep
        rate.sleep()

    camera.release()
    print('cv bye ...')


def subscribe2(**kwargs):
    geckopy = GeckoPy()

    def f(t, m):
        # print('>> Message[{}]'.format(t))
        chew_up_cpu()
        chew_up_cpu()
        chew_up_cpu()
        chew_up_cpu()
        pass

    topic = kwargs.get('topic', 'test')
    s = geckopy.Subscriber([topic], f)
    geckopy.spin(20)


if __name__ == "__main__":
    # you can also run this file and it will run the function
    # alows modular development, don't have to run the whole gecko infrastructure
    # to test something ... but a lot may not happen though :)
    kw = {'topic': 'hello'}
    # publish(kwargs=kw)
    # pvc(kwargs=kw)
    subscribe2(kwargs=kw)
