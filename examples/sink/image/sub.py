#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
from pygecko.multiprocessing import geckopy
import cv2
# from pygecko import Image
from pygecko import msg2image
import numpy as np
import platform
import time


def subscriber(**kwargs):
    geckopy.init_node(**kwargs)

    def callback(topic, msg):
        # print('msg',msg.shape)
        # img = np.frombuffer(msg.bytes, dtype=np.uint8)
        # img = img.reshape(msg.shape)
        img = msg2image(msg)
        geckopy.logdebug('image timestamp: {:.3f}'.format(msg.timestamp))
        cv2.imshow('image',img)
        key = cv2.waitKey(1)

    geckopy.Subscriber(['camera'], callback)

    geckopy.spin(20) # it defaults to 100hz, this is just to slow it down
    print('sub bye ...')


if __name__ == '__main__':

    args = {
        'geckocore': {
            'host': 'localhost'
        }
    }
    subscriber(**args)
