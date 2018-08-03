#!/usr/bin/env python3

#
#
# copyright Kevin Walchko
#
# Basically a rostopic

from __future__ import print_function
import argparse
import time
# from pygecko import TopicSub
from pygecko.transport import zmqTCP, GeckoCore
from pygecko.multiprocessing import GeckoPy
from pygecko.test import GeckoSimpleProcess
# from pygecko.transport.zmqclass import 

# def publisher(**kwargs):
#     geckopy = GeckoPy()
#
#     p = geckopy.Publisher()
#
#     hertz = kwargs.get('rate', 10)
#     rate = geckopy.Rate(hertz)
#
#     topic = kwargs.get('topic')
#     msg = kwargs.get('msg')
#
#     cnt = 0
#     start = time.time()
#     while not geckopy.is_shutdown():
#         p.pub(topic, msg)  # topic msg
#         if cnt % hertz == 0:
#             print(">> {}[{:.1f}]: published {} msgs".format(topic, time.time()-start, hertz))
#         cnt += 1
#         rate.sleep()


def subscriber(**kwargs):
    geckopy = GeckoPy(**kwargs)

    def f(topic, msg):
        print(">> {}: {}".format(topic, msg))

    topic = kwargs.get('topic')
    s = geckopy.Subscriber([topic], f)

    geckopy.spin()


if __name__ == '__main__':
    p = GeckoSimpleProcess()
    p.start(func=subscriber, name='subscriber', kwargs=args)

    # while True:
    #     try:
    #         time.sleep(1)
    #     except KeyboardInterrupt:
    #         break
    #
    # # shutdown the processes
    # p.join(0.1)
