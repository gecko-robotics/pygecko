#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

from pygecko.multiprocessing import geckopy
from pygecko.multiprocessing import GeckoSimpleProcess
from imutils.video import VideoStream
import cv2
from pygecko import Image
import numpy as np


# class Callback(object):
#     def __init__(self):
#         self.jar = PickleJar('test.pickle')
#     def callback(self, topic, msg):
#         geckopy.loginfo("recv[{}]: {}".format(topic, msg))
#         self.jar.push(msg)
#

def callback(topic, msg):
    img = np.frombytes(msg.d, dtype=np.uint8)
    img.reshape(msg.shape)
    cv2.imshow(img)
    key = cv2.waitKey(10)


def subscriber(**kwargs):
    geckopy.init_node(**kwargs)
    geckopy.Subscriber(['camera'], callback)

    geckopy.spin(20) # it defaults to 100hz, this is just to slow it down
    print('sub bye ...')


def publisher(**kwargs):
    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(10)  # 10 Hz

    p = geckopy.Publisher()

    # determine if we should use picamera or standard usb camera
    if platform.system() == 'Linux':
        picam = True
    else:
        picam = False

    camera = VideoStream(usePiCamera=picam, resolution=(320, 240), framerate=10)

    while not geckopy.is_shutdown():
        img = camera.read()
        img = cv2.CvtColor(img, cv2.COLOR_BGR2GRAY)
        msg = Image(img.shape, img.tobytes())
        p.pub('camera', msg)
        rate.sleep()

    print('pub bye ...')


if __name__ == '__main__':
    args = {}
    p = GeckoSimpleProcess()
    p.start(func=publisher, name='cam_pub', kwargs=args)

    s = GeckoSimpleProcess()
    s.start(func=subscriber, name='ca_sub', kwargs=args)
