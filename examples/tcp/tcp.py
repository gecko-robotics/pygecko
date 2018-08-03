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
    geckopy = GeckoPy(**kwargs)
    rate = geckopy.Rate(2)

    p = geckopy.Publisher()
    start = time.time()
    topic = kwargs.get('topic')
    cnt = 0
    while not geckopy.is_shutdown():
        msg = {'time': time.time() - start}
        p.pub(topic, msg)  # topic msg

        geckopy.log('[{}] published msg'.format(cnt))
        cnt += 1
        rate.sleep()
    print('pub bye ...')


def subscriber(**kwargs):
    geckopy = GeckoPy(**kwargs)

    def f(topic, msg):
        # print("recv[{}]: {}".format(topic, msg))
        geckopy.log(msg)
        chew_up_cpu()
        chew_up_cpu()
        chew_up_cpu()
        chew_up_cpu()

    topic = kwargs.get('topic')
    s = geckopy.Subscriber([topic], f)

    geckopy.spin(20) # it defaults to 100hz, this is just to slow it down
    print('sub bye ...')


if __name__ == '__main__':
    # normally you wouldn't run this here, but is running else where
    # this is just for testing
    # core = GeckoCore()
    # core.start()
    procs = []
    for topic in ['ryan', 'mike', 'sammie', 'scott']:
    # for topic in ['ryan']:
        # info to pass to processes
        args = {
            'topic': topic
        }

        p = GeckoSimpleProcess()
        p.start(func=publisher, name='publisher {}'.format(topic), kwargs=args)
        procs.append(p)

        s = GeckoSimpleProcess()
        s.start(func=subscriber, name='subscriber {}'.format(topic), kwargs=args)
        procs.append(s)

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('main process got ctrl-c')
            break
