#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
from pygecko.transport.core import GeckoCore
from pygecko.multiprocessing import geckopy
from pygecko.multiprocessing import GeckoSimpleProcess
import cv2
from pygecko import Image
import numpy as np
import platform
import time


# def callback(topic, msg):
#     img = np.frombytes(msg.d, dtype=np.uint8)
#     img.reshape(msg.shape)
#     cv2.imshow(img)
#     key = cv2.waitKey(10)


def subscriber(**kwargs):
    geckopy.init_node(**kwargs)

    def callback(topic, msg):
        # print('msg',msg.shape)
        img = np.frombuffer(msg.bytes, dtype=np.uint8)
        img = img.reshape(msg.shape)
        print('image[{}]'.format(msg.timestamp,img.shape))
        cv2.imshow('image',img)
        key = cv2.waitKey(1)

    geckopy.Subscriber(['camera'], callback)

    geckopy.spin(20) # it defaults to 100hz, this is just to slow it down
    print('sub bye ...')


# def publisher(**kwargs):
#     from imutils.video import VideoStream
#     geckopy.init_node(**kwargs)
#     rate = geckopy.Rate(10)  # 10 Hz
#
#     p = geckopy.Publisher()
#
#     # determine if we should use picamera or standard usb camera
#     if platform.system() == 'Linux':
#         picam = True
#     else:
#         picam = False
#
#     # camera = VideoStream(usePiCamera=picam, resolution=(320, 240), framerate=10)
#     camera = cv2.VideoCapture(0)
#
#     while not geckopy.is_shutdown():
#         ok,img = camera.read()
#         img = cv2.CvtColor(img, cv2.COLOR_BGR2GRAY)
#         msg = Image(img.shape, img.tobytes())
#         p.pub('camera', msg)
#         rate.sleep()
#
#     print('pub bye ...')


if __name__ == '__main__':
    # core = GeckoCore()
    # core.start()

    args = {}
    subscriber(**args)
    # p = GeckoSimpleProcess()
    # p.start(func=publisher, name='cam_pub', kwargs=args)

    # s = GeckoSimpleProcess()
    # s.start(func=subscriber, name='ca_sub', kwargs=args)
    #
    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     pass
