#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2014 Kevin Walchko
# see LICENSE for full details
##############################################

import argparse
import sys
import tty
import termios
# from pygecko.transport import zmqTCP, zmqUDS
from pygecko.multiprocessing import geckopy
from pygecko.multiprocessing.geckopy import pubBinderTCP
from pygecko.multiprocessing.geckopy import pubBinderUDS
# import time

######################################################
# move to messages
# from collections import namedtuple
from pygecko.messages import vec_t
from pygecko.messages import twist_t

######################################################


def limit_max(x):
    x = 1.0 if x > 1.0 else x
    return x


def limit_min(x):
    x = -1.0 if x < -1.0 else x
    return x


def publisher(**kwargs):
    geckopy.init_node()
    rate = geckopy.Rate(10)

    tcp = kwargs["useTcp"]
    key = kwargs["key"]

    if tcp:
        p = pubBinderTCP(key, 'twist_kb')
    else:
        p = pubBinderUDS(key, 'twist_kb', fname=kwargs["udsfile"])

    if p is None:
        return

    ang = [0, 0, 0]
    lin = [0, 0, 0]

    while not geckopy.is_shutdown():

        # have to do some fancy stuff to avoid sending \n all the time
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        if key not in ['a', 'd', 'w', 'x', 's', 'q']:
            continue

        print('>>>', key)

        if key == 'a':
            ang[2] += 0.1
            ang[2] = limit_max(ang[2])
        elif key == 'd':
            ang[2] -= 0.1
            ang[2] = limit_min(ang[2])
        elif key == 'w':
            lin[0] += 0.1
            lin[0] = limit_max(lin[0])
        elif key == 'x':
            lin[0] -= 0.1
            lin[0] = limit_min(lin[0])
        elif key == 's':  # stop - all 0's
            ang = [0, 0, 0]
            lin = [0, 0, 0]
        elif key == 'q':
            break

        twist = twist_t(vec_t(*lin), vec_t(*ang))
        p.publish(twist)  # topic msg
        rate.sleep()


# set up and handle command line args
def handleArgs():
    parser = argparse.ArgumentParser(description='A simple zero MQ publisher for keyboard messages')

    feature_parser = parser.add_mutually_exclusive_group(required=False)
    feature_parser.add_argument('--tcp', dest='useTcp', action='store_true', help="enable TCP communication [default]")
    feature_parser.add_argument('--uds', dest='useTcp', action='store_false', help="enable UDS communication")
    parser.set_defaults(useTcp=True)

    # parser.add_argument('-p', '--publish', nargs=2, help='publish messages to addr:port, ex. js 10.1.1.1 9000', default=['localhost', '9000'])
    parser.add_argument('key', help='geckocore machine key')
    parser.add_argument('-f', '--file', help='UDS file', default='/tmp/twist_kb')
    # parser.add_argument('-v', '--verbose', help='display info to screen', action='store_true')
    args = vars(parser.parse_args())
    return args


def main():
    args = handleArgs()
    kwargs = {
        "key": args["key"],
        "useTcp": args["useTcp"],
        "udsfile": args["file"]  # args["udsfile"]
    }

    # print('Twist Keyboard on {}:{}'.format(args['publish'][0], args['publish'][1]))

    print('------------------------')
    print(' q - quit')
    print('------------------------')
    print(' w - forward')
    print(' a/d - left/right')
    print(' x - reverse')
    print(' s - stop')
    print('------------------------')

    publisher(**kwargs)


if __name__ == "__main__":
    main()
