#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

from __future__ import print_function
# from pygecko.transport import zmqTCP
from pygecko.multiprocessing import geckopy
# from pygecko.test import GeckoSimpleProcess
# from pygecko import Lidar
# import time
from pltslamshow import SlamShow
from sslam import RMHC_SLAM
from sslam import LDS01_Model


def subscriber(**kwargs):
    geckopy.init_node(**kwargs)

    MAP_SIZE_PIXELS = 500
    MAP_SIZE_METERS = 10
    slam = RMHC_SLAM(LDS01_Model(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)
    display = SlamShow(MAP_SIZE_PIXELS, MAP_SIZE_METERS*1000/MAP_SIZE_PIXELS, 'SLAM')
    mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)

    # callback function
    def f(topic, msg):
        # print("recv[{}]: {}".format(topic, msg))
        geckopy.log(msg.timestamp)
        pts = msg.scan
        slam.update(pts)

        # Get current robot position
        x, y, theta = slam.getpos()

        # Get current map bytes as grayscale
        slam.getmap(mapbytes)

        display.displayMap(mapbytes)
        display.setPose(x, y, theta)
        display.refresh()

    geckopy.Subscriber(['scan'], f)

    geckopy.spin(20) # it defaults to 100hz, this is just to slow it down
    print('sub bye ...')


if __name__ == '__main__':
    # so matplotlib seems to call something early and multiprocessing with it
    # has issues
    subscriber()
