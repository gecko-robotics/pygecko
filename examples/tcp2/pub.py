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

    p = geckopy.pubBinderTCP(
        kwargs.get('key'),
        kwargs.get('topic')

    )
    if p is None:
        raise Exception("publisher is None")

    start = time.time()
    cnt = 0
    while not geckopy.is_shutdown():
        msg = {'time': time.time() - start}
        p.publish(msg)  # topic msg

        geckopy.logdebug('[{}] published msg'.format(cnt))
        cnt += 1
        rate.sleep()
    print('pub bye ...')

# def subscriber(**kwargs):
#     geckopy.init_node(**kwargs)
#     rate = geckopy.Rate(2)
#
#     topic = kwargs.get('topic')
#     # c = Callback(topic)
#     s = geckopy.subConnectTCP(
#         kwargs.get('key'),
#         kwargs.get('topic')
#     )
#     if s is None:
#         raise Exception("subscriber is None")
#
#     while not geckopy.is_shutdown():
#         msg = s.recv_nb()
#         if msg:
#             geckopy.loginfo("{}: {}".format(topic,msg))
#         chew_up_cpu(.1)
#         rate.sleep()
#
#     print('sub bye ...')


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

    for topic in ['ryan', 'mike', 'sammie', 'scott']:
        # info to pass to processes
        args = {
            "key": "local",
            'topic': topic
        }

        p = GeckoSimpleProcess()
        p.start(func=publisher, name='pub_{}'.format(topic), kwargs=args)
        procs.append(p)

        # s = GeckoSimpleProcess()
        # s.start(func=subscriber, name='sub_{}'.format(topic), kwargs=args)
        # procs.append(s)

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('main process got ctrl-c')
            break
