# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2014 Kevin Walchko
# see LICENSE for full details
##############################################
#
from pygecko.multiprocessing import geckopy
import cv2
from pygecko import msg2image


def subscriber(**kwargs):
    geckopy.init_node(**kwargs)

    def callback(topic, msg):
        img = msg2image(msg)
        geckopy.logdebug('image timestamp: {:.3f}'.format(msg.timestamp))
        cv2.imshow('image',img)
        cv2.waitKey(10)

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
