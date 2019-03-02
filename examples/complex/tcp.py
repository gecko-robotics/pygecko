#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################

from pygecko.multiprocessing import geckopy
from pygecko.multiprocessing import GeckoSimpleProcess
import time


def chew_up_cpu(interval):
    # chew up some cpu
    start = time.time()
    while (time.time() - start) < interval: 5*5



def publisher(**kwargs):
    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(2)

    topic = kwargs.get('topic')
    p = geckopy.pubBinderTCP(kwargs.get('key'),topic)
    start = time.time()
    cnt = 0
    while not geckopy.is_shutdown():
        msg = cnt
        p.publish(msg)  # topic msg

        geckopy.logdebug('{}[{}] published msg'.format(topic,cnt))
        cnt += 1
        rate.sleep()
    print('pub bye ...')


class Callback(object):
    """
    So the idea here is instead of using a simple callback function
    like what is commented out above, I need to setup some stuff
    and have it available during the callback. A simple class
    allows me to do this
    """
    def __init__(self, name):
        self.name = name
        self.r = 0
        self.s = 0

    def loop(self, **kwargs):
        geckopy.init_node(**kwargs)
        rate = geckopy.Rate(2)

        sr = geckopy.subConnectTCP(kwargs.get('key'),'ryan')
        ss = geckopy.subConnectTCP(kwargs.get('key'),'scott')
        p = geckopy.pubBinderTCP(kwargs.get('key'),'ans')

        start = time.time()
        while not geckopy.is_shutdown():
            m = sr.recv_nb()
            if m:
                self.r = m

            m = ss.recv_nb()
            if m:
                self.s = m

            msg = {'ans': self.s + self.r}
            p.publish(msg)  # topic msg

            geckopy.logdebug('ans msg: {}'.format(msg))
            rate.sleep()
        print('pub bye ...')


if __name__ == '__main__':
    # normally you wouldn't run this here, but is running else where
    # this is just for testing
    # from pygecko.transport import GeckoCore
    # core = GeckoCore()
    # core.start()

    # although I don't do anything with procs, because I reuse the variables
    # p and s below, they will kill the processes when new process are created
    # using those names. Appending them to procs allows me to keep them alive
    # until the program ends
    procs = []

    for topic in ['ryan','scott']:
        # info to pass to processes
        args = {
            'key': "local",
            'topic': topic
        }

        p = GeckoSimpleProcess()
        p.start(func=publisher, name='pub_{}'.format(topic), kwargs=args)
        procs.append(p)


    args = {
        'key': "local"
    }
    s = GeckoSimpleProcess()
    c = Callback('class')
    s.start(func=c.loop, name='sub', kwargs=args)
    procs.append(s)

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('main process got ctrl-c')
            break
