#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################

from pygecko.multiprocessing import geckopy
from pygecko.multiprocessing import GeckoSimpleProcess
from pygecko.transport.protocols import MsgPack, MsgPackCustom
import time
from math import cos, pi




def pub(**kwargs):
    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(2)

    p = geckopy.pubBinderTCP("local", "bob")
    if (p == None):
        print("ERROR setting up publisher")
        return
    cnt = 0
    while not geckopy.is_shutdown():
        # msg = "hi" + str(cnt)
        msg = [pi, cos(pi), cos(pi/2,)]
        p.publish(msg)
        print("sent")
        rate.sleep()
        cnt += 1


def sub(**kwargs):
    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(2)

    s = geckopy.subConnectTCP("local", "bob")
    if (s == None):
        print("ERROR setting up subscriber")
        return
    cnt = 0
    while not geckopy.is_shutdown():
        data = s.recv_nb()
        print("sub:", data)
        rate.sleep()


if __name__ == '__main__':
    args = {}
    p = GeckoSimpleProcess()
    p.start(func=pub, name='pub', kwargs=args)

    s = GeckoSimpleProcess()
    s.start(func=sub, name='sub', kwargs=args)
