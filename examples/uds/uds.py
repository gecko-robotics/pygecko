#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#


from __future__ import print_function

# fix path for now
# import sys
# sys.path.append("../../")

# from pygecko.transport import Pub, Sub
from pygecko.transport import zmqTCP, GeckoCore, zmqUDS
from pygecko.multiprocessing import geckopy
from pygecko.test import GeckoSimpleProcess

import time
import signal
import os


def publish(**kwargs):
    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(2)

    print('pub', kwargs)

    topic = kwargs.get('topic', 'test')
    addr = kwargs.get('pub_uds', None)
    print('publish addr:', addr)

    p = geckopy.Publisher(addr=addr)

    while not geckopy.is_shutdown():
        msg = {'s': time.time()}
        p.pub(topic, msg)  # topic msg

        rate.sleep()

    geckopy.log('pub bye ...')


def subscribe(**kwargs):
    geckopy.init_node(**kwargs)

    def f(t, m):
        geckopy.log('>> Message[{}]'.format(t))

    topic = kwargs.get('topic', 'test')
    addr = kwargs.get('sub_uds', None)
    print('subscriber addr:', addr)

    s = geckopy.Subscriber([topic], f, addr=addr)
    geckopy.spin(20)
    geckopy.log('sub bye ...')


if __name__ == '__main__':
    # info to pass to processes
    args = {
        'topic': 'hi'
    }

    args['pub_uds'] = zmqUDS('/tmp/uds_ifile')
    args['sub_uds'] = zmqUDS('/tmp/uds_ofile')

    # this is sort of like crossing RX/TX lines here
    #        +---------+
    # pub -> | in  out | -> sub
    #        +---------+
    core = GeckoCore(
        in_addr=zmqUDS(args['pub_uds']),
        out_addr=zmqUDS(args['sub_uds'])
    )
    core.start()

    p = GeckoSimpleProcess()
    p.start(func=publish, name='publisher', kwargs=args)

    s = GeckoSimpleProcess()
    s.start(func=subscribe, name='subscriber', kwargs=args)


    print("\n\n<<< press ctrl-c to exit >>>\n\n")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('main process got ctrl-c')
            break

    s.join(0.1)
    p.join(0.1)
    core.join(0.1)
