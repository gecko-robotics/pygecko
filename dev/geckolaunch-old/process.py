#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import multiprocessing as mp
import time
import signal
import imutils

# fix path for now
# once gecko is installed you don't need this kludge
# import sys
# sys.path.append("../../")

from pygecko.transport import Pub, Sub
# from pygecko.transport.zmqclass import SubNB
from pygecko.transport import zmqTCP  #, GeckoCore
from pygecko.multiprocessing import GeckoPy
from math import sin, cos, pi, sqrt
import numpy as np

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
    geckopy = GeckoPy(**kwargs)
    rate = geckopy.Rate(1)

    topic = kwargs.get('topic', 'test')

    p = geckopy.Publisher()
    datumn = time.time()
    while not geckopy.is_shutdown():
        msg = {'time': time.time() - datumn, 'double': 3.14, 'int': 5, 'array': [1, 2, 3, 4, 5]}
        p.pub(topic, msg)
        # print('>> published msg on topic {}'.format(topic))

        # chew up some cpu
        # chew_up_cpu()

        # sleep
        rate.sleep()

    print('pub bye ...')


def pcv(**kwargs):
    geckopy = GeckoPy(**kwargs)
    rate = geckopy.Rate(1)

    topic = kwargs.get('topic', 'test')

    p = geckopy.Publisher()

    # camera = cv2.VideoCapture(0)
    from imutils.video import WebcamVideoStream
    # camera.set(3, 640)
    # camera.set(4, 480)
    # camera.set(3, 320)
    # camera.set(4, 240)
    camera = WebcamVideoStream(src=0).start()

    datumn = time.time()

    while not geckopy.is_shutdown():
        # start = time.time()
        # ok, img = camera.read()
        ok, img = True, camera.read()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # img = cv2.resize(img,(640,480))
        # end = time.time()
        # print("* camera time: {}".format(end - start))
        if ok:
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            shape = img.shape
            dtype = img.dtype
            img = img.tobytes()
            msg = {'img': img, 'shape': shape, 'dtype': dtype, 'stamp': time.time() - datumn}
            p.pub(topic, msg)  # topic msg
            # p.pub(topic, {'a': 5})
        else:
            print("*** couldn't read image ***")

        # sleep
        rate.sleep()

    # camera.release()
    camera.stop()
    print('cv bye ...')


def subscribe2(**kwargs):
    geckopy = GeckoPy(**kwargs)

    def f(t, m):
        # print('>> Message[{}]'.format(t))
        if 'img' in m:
            im = m['img']
            im = np.frombuffer(im, dtype=m['dtype'])
            im = im.reshape(m['shape'])
            geckopy.log('image: {}x{}'.format(*im.shape[:2]))
            # if im.shape != (480, 640):
            #     print("*** image shape wrong: {} ***".format(im.shape))
        else:
            geckopy.log('msg: {}'.format(m))
            chew_up_cpu()
            chew_up_cpu()
            chew_up_cpu()
            chew_up_cpu()

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
