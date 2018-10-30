#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
from pygecko.multiprocessing import geckopy
import cv2
from pygecko import image2msg
import platform
from imutils.video import VideoStream


def publisher(**kwargs):
    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(10)  # 10 Hz

    p = geckopy.Publisher(['camera'])

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
        # img = cv2.resize(img, (640, 480))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        msg = image2msg(img)
        p.pub('camera', msg)
        rate.sleep()

    print('pub bye ...')


if __name__ == '__main__':
    args = {"host": "localhost"}
    publisher(**args)
