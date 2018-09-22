#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################

from pygecko.multiprocessing import geckopy
from pygecko.test import GeckoSimpleProcess
import time


def chew_up_cpu(interval):
    # chew up some cpu
    start = time.time()
    while (time.time() - start) < interval:
        5*5


def pub_bye():
    print("-"*30)
    print(" Publisher shutting down ...")
    print("-"*30)


def publisher(**kwargs):
    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(2)
    geckopy.on_shutdown(pub_bye)

    p = geckopy.Publisher()
    start = time.time()
    topic = kwargs.get('topic')
    cnt = 0
    while not geckopy.is_shutdown():
        msg = {'time': time.time() - start}
        p.pub(topic, msg)  # topic msg

        geckopy.logdebug('[{}] published msg'.format(cnt))
        cnt += 1
        rate.sleep()
    print('pub bye ...')



# def f(topic, msg):
#     # print("recv[{}]: {}".format(topic, msg))
#     geckopy.log(msg)
#     chew_up_cpu(.1)

class Callback(object):
    """
    So the idea here is instead of using a simple callback function
    like what is commented out above, I need to setup some stuff
    and have it available during the callback. A simple class
    allows me to do this
    """
    def __init__(self, name):
        self.name = name
    def callback(self, topic, msg):
        geckopy.loginfo("{}".format(msg))
        chew_up_cpu(.1)
    def bye(self):
        print("*"*30)
        print(" {} shutting down ...".format(self.name))
        print("*"*30)

def subscriber(**kwargs):
    geckopy.init_node(**kwargs)


    topic = kwargs.get('topic')
    c = Callback(topic)
    geckopy.Subscriber([topic], c.callback)
    geckopy.on_shutdown(c.bye)

    geckopy.spin(20) # it defaults to 100hz, this is just to slow it down
    print('sub bye ...')


if __name__ == '__main__':
    # normally you wouldn't run this here, but is running else where
    # this is just for testing
    # core = GeckoCore()
    # core.start()

    # although I don't do anything with procs, because I reuse the variables
    # p and s below, they will kill the processes when new process are created
    # using those names. Appending them to procs allows me to keep them alive
    # until the program ends
    procs = []

    for topic in ['ryan', 'mike', 'sammie', 'scott']:
        # info to pass to processes
        # args = {
        #     'topic': topic,
        #     "geckocore": {
        #         "key": "multiped"
        #     }
        # }

        # args = {
        #     'topic': topic,
        #     "geckocore": {
        #         "type": "tcp",
        #         "in": ["multiped.local", 9998],
        #         "out": ["multiped.local", 9999]
        #     }
        # }

        args = {
            'topic': topic,
            "geckocore":{
                # this can be tcp or uds address for zmq
                "in_addr": "tcp://multiped.local:9998",
                "out_addr": "tcp://multiped.local:9999"
            }
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
