#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
from pygecko.transport.core import GeckoCore
from pygecko.multiprocessing import geckopy
from pygecko.multiprocessing import GeckoSimpleProcess
import cv2
from pygecko import image2msg
import numpy as np
import platform
import time
from imutils.video import VideoStream


# def callback(topic, msg):
#     img = np.frombytes(msg.d, dtype=np.uint8)
#     img.reshape(msg.shape)
#     cv2.imshow(img)
#     key = cv2.waitKey(10)


# def subscriber(**kwargs):
#     geckopy.init_node(**kwargs)
#
#     # cv2.imshow('image', None)
#
#     def callback(topic, msg):
#         img = np.frombuffer(msg.bytes, dtype=np.uint8)
#         img = img.reshape(msg.shape)
#         cv2.imshow('image', img)
#         key = cv2.waitKey(1)
#
#     geckopy.Subscriber(['camera'], callback)
#
#     geckopy.spin(20) # it defaults to 100hz, this is just to slow it down
#     print('sub bye ...')


def publisher(**kwargs):
    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(10)  # 10 Hz

    p = geckopy.Publisher()

    # determine if we should use picamera or standard usb camera
    if platform.system() == 'Linux':
        picam = True
    else:
        picam = False

    camera = VideoStream(usePiCamera=picam)
    camera.start()

    while not geckopy.is_shutdown():
        img = camera.read()
        # img = cv2.resize(img, (320, 240))
        img = cv2.resize(img, (640, 480))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # msg = Image(img.shape, img.tobytes())
        msg = image2msg(img)
        p.pub('camera', msg)
        rate.sleep()

    print('pub bye ...')


if __name__ == '__main__':
    # core = GeckoCore()
    # core.start()

    args = {}
    # p = GeckoSimpleProcess()
    # p.start(func=publisher, name='cam_pub', kwargs=args)

    # s = GeckoSimpleProcess()
    # s.start(func=subscriber, name='ca_sub', kwargs=args)

    publisher(**args)

    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     pass
