#!/usr/bin/env python3
#


from __future__ import print_function

# fix path for now
import sys
sys.path.append("../../")

# from pygecko.transport import Pub, Sub
from pygecko.transport import zmqTCP, GeckoCore, zmqUDS
from pygecko.multiprocessing import GeckoPy
from pygecko.test import GeckoSimpleProcess

import time
import signal
import os


def publish(**kwargs):
    geckopy = GeckoPy()
    rate = geckopy.Rate(2)

    print('pub', kwargs)

    topic = kwargs.get('topic', 'test')
    fname = kwargs.get('pub_uds', None)
    print('fname', fname)

    p = geckopy.Publisher(uds_file=fname)

    while not geckopy.is_shutdown():
        msg = {'s': time.time()}
        p.pub(topic, msg)  # topic msg

        rate.sleep()

    print('pub bye ...')


def subscribe(**kwargs):
    geckopy = GeckoPy()

    def f(t, m):
        print('>> Message[{}]'.format(t))

    topic = kwargs.get('topic', 'test')
    fname = kwargs.get('sub_uds')

    s = geckopy.Subscriber([topic], f, uds_file=fname)
    geckopy.spin(20)
    print('sub bye ...')


if __name__ == '__main__':
    # info to pass to processes
    args = {
        'topic': 'hi',
        'sub_uds': '/tmp/uds_ofile',
        'pub_uds': '/tmp/uds_ifile',
    }

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
