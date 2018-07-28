#!/usr/bin/env python3
#

from __future__ import print_function

# fix path for now, once gecko is installed you don't need this
import sys
sys.path.append("../../")

# from pygecko.transport import Pub, Sub
from pygecko.transport import zmqTCP, GeckoCore
from pygecko.multiprocessing import GeckoPy
from pygecko.test import GeckoSimpleProcess

from math import sin, cos, pi, sqrt
import time


def chew_up_cpu():
    # chew up some cpu
    for i in range(90):
        m = sin(i*pi/180)*cos(i*pi/180)*sin(i*pi/180)*cos(i*pi/180)*sin(i*pi/180)*cos(i*pi/180)
        sqrt(m**9)


def publisher(**kwargs):
    geckopy = GeckoPy()
    rate = geckopy.Rate(2)

    p = geckopy.Publisher()

    topic = kwargs.get('topic')
    while not geckopy.is_shutdown():
        msg = {'time': time.time()}
        p.pub(topic, msg)  # topic msg

        # print('[{}] published msg'.format(cnt))
        rate.sleep()
    print('pub bye ...')


def subscriber(**kwargs):
    geckopy = GeckoPy()

    def f(topic, msg):
        # print("recv[{}]: {}".format(topic, msg))
        chew_up_cpu()
        chew_up_cpu()
        chew_up_cpu()
        chew_up_cpu()

    topic = kwargs.get('topic')
    s = geckopy.Subscriber([topic], f)

    geckopy.spin(10)
    print('sub bye ...')


if __name__ == '__main__':
    # normally you wouldn't run this here, but is running else where
    # this is just for testing
    core = GeckoCore()
    core.start()

    # keep track of the processes we create
    procs = []

    for topic in ['ryan', 'mike', 'sammie', 'scott']:
        # info to pass to processes
        args = {
            'topic': topic
        }

        p = GeckoSimpleProcess()
        p.start(func=publisher, name='publisher', kwargs=args)
        procs.append(p)

        p = GeckoSimpleProcess()
        p.start(func=subscriber, name='subscriber', kwargs=args)
        procs.append(p)


    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('main process got ctrl-c')
            break

    # shutdown the processes
    for p in procs:
        p.join(0.1)

    # shut down the core
    core.join(0.1)
