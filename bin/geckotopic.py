#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2014 Kevin Walchko
# see LICENSE for full details
##############################################
# Basically a rostopic

import argparse
import time
# from pygecko import TopicSub
# from pygecko.transport import zmqTCP, GeckoCore
from pygecko.multiprocessing import geckopy
from pygecko.test import GeckoSimpleProcess

try:
    import simplejson as json
except ImportError:
    import json


def handleArgs():
    parser = argparse.ArgumentParser(description="""
    A simple zero MQ message tool. It will subscribe to a topic and print the messages.

    Format:
        topic_echo host port topic

    geckotopic mode[0] mode[1] [options]
    geckotopic pub <topic-name> -m [data...]
    geckotopic echo <topic-name>

    Examples:
        geckotopic echo hello
        geckotopic pub hello "{'a': 3.14, 'k': [1,2,3,4]}"
    """)
    parser.add_argument('-m', '--msg', help='data to publish', default=None)
    parser.add_argument('-r', '--rate', help='publish rate in hertz, default 10 hz', default=10)
    # parser.add_argument('-o', '--once', help='publish a message once and exit')
    parser.add_argument('mode', nargs=2, help="run geckotopic as pub (publisher of topic), echo (subscribed to topic)", default=None)
    # parser.add_argument('-i', '--info', nargs=2, help='subscribe to messages on host port: ex. 1.2.3.4 9000', default=None)
    # parser.add_argument('-v', '--verbose', help='display info to screen', action='store_true')
    args = vars(parser.parse_args())
    return args


def publisher(**kwargs):
    geckopy.init_node(**kwargs)

    topic = kwargs.get('topic')
    msg = kwargs.get('msg')
    hertz = kwargs.get('rate', 10)

    p = geckopy.Publisher([topic])

    rate = geckopy.Rate(hertz)

    cnt = 0
    start = time.time()
    while not geckopy.is_shutdown():
        p.pub(topic, msg)  # topic msg
        if cnt % hertz == 0:
            print(">> {}[{:.1f}]: published {} msgs".format(topic, time.time()-start, hertz))
        cnt += 1
        rate.sleep()


def subscriber(**kwargs):
    # geckopy = GeckoPy()
    geckopy.init_node(**kwargs)

    def f(topic, msg):
        print(">> {}: {}".format(topic, msg))

    topic = kwargs.get('topic')
    geckopy.Subscriber([topic], f)

    geckopy.spin()


if __name__ == '__main__':
    args = handleArgs()

    if args['mode'] is None or args['mode'][0] not in ['pub', 'echo', 'list']:
        print("Error: please do geckotopic --help")  # FIXME: print help

    if args['mode'] == 'list':
        raise NotImplementedError()

    args['topic'] = args['mode'][1]

    if args['msg'] is not None:
        msg = args['msg']
        args['msg'] = json.loads(args['msg'].replace("'", '"'))
        print(args['msg'])
        print(type(args['msg']))

    # check port > 8000
    # check valid host?
    # if  args['info'] is not None:
    #     args['host_port'] = (args['info'][0], args['info'][1])

    if args['mode'][0] == 'pub':
        p = GeckoSimpleProcess()
        p.start(func=publisher, name='publisher', kwargs=args)
    elif args['mode'][0] == 'echo':
        p = GeckoSimpleProcess()
        p.start(func=subscriber, name='subscriber', kwargs=args)

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    # shutdown the processes
    p.join(0.1)
