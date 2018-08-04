#!/usr/bin/env python3

#
# by Kevin J. Walchko 6 Aug 2016
#


from __future__ import print_function
from __future__ import division
import argparse
import sys
import tty
import termios
# from pygecko import ZmqClass as Zmq
from pygecko.transport import zmqTCP, GeckoCore
from pygecko.multiprocessing import geckopy
from pygecko.test import GeckoSimpleProcess
import time

######################################################
# move to messages
from collections import namedtuple
from the_collector.messages import Vector

Twist = namedtuple('Twist', 'linear angular')

######################################################


def limit_max(x):
    x = 1.0 if x > 1.0 else x
    return x


def limit_min(x):
    x = -1.0 if x < -1.0 else x
    return x


def publisher(**kwargs):
    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(10)

    p = geckopy.Publisher()

    a = [0,0,0]
    l = [0,0,0]

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
            a[2] += 0.1
            a[2] = limit_max(a[2])
        elif key == 'd':
            a[2] -= 0.1
            a[2] = limit_min(a[2])
        elif key == 'w':
            l[0] += 0.1
            l[0] = limit_max(l[0])
        elif key == 'x':
            l[0] -= 0.1
            l[0] = limit_min(l[0])
        elif key == 's':  # stop - all 0's
            a = [0,0,0]
            l = [0,0,0]
        elif key == 'q':
            break

        twist = Twist(Vector(*a), Vector(*l))
        # twist = [a,l]  # FIXME: use a real message
        p.pub('twist_kb', twist)  # topic msg
        rate.sleep()


# set up and handle command line args
def handleArgs():
    parser = argparse.ArgumentParser(description='A simple zero MQ publisher for keyboard messages')
    parser.add_argument('-p', '--publish', nargs=2, help='publish messages to addr:port, ex. js 10.1.1.1 9000', default=['localhost', '9000'])
    # parser.add_argument('-v', '--verbose', help='display info to screen', action='store_true')
    args = vars(parser.parse_args())
    return args


def main():
    args = handleArgs()

    # print('Twist Keyboard on {}:{}'.format(args['publish'][0], args['publish'][1]))

    print('------------------------')
    print(' q - quit')
    print('------------------------')
    print(' w - forward')
    print(' a/d - left/right')
    print(' x - reverse')
    print(' s - stop')
    print('------------------------')

    publisher(**args)


if __name__ == "__main__":
    main()
