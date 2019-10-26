#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2014 Kevin Walchko
# see LICENSE for full details
##############################################

import argparse
import sys


def handleArgs():
    parser = argparse.ArgumentParser(description='test program')
    # parser.add_argument('file', help='launch file')
    # parser.add_argument('-f', '--format', help='format: json or yaml, default is json', default='json')

    subparsers = parser.add_subparsers()

    # Bag ------------------------------------------------------------------
    b_p = subparsers.add_parser('bag', description='bag help')
    b_p.add_argument("mode", help="play,record")
    b_p.add_argument("filename")
    b_p.add_argument("topic")
    b_p.add_argument("-l", '--loop', help="loop")

    # Topic -----------------------------------------------------------------
    t_p = subparsers.add_parser('topic', description='topic help')
    t_p.add_argument("mode", help="echo, bw, pub")
    t_p.add_argument("topic")
    # t_p.add_argument("-l", '--loop', help="loop")

    # Multicast --------------------------------------------------------------
    m_p = subparsers.add_parser('multicast', description='multicast help')
    m_p.add_argument("mode", help="send or receive")
    # m_p.add_argument("topic")

    # Core ------------------------------------------------------------------
    m_p = subparsers.add_parser('core', description='core help')
    m_p.add_argument("mode", help="run or alive")

    # Gecko ----------------------------------------------------------------
    parser.add_argument('-k', '--key', help="key for the geckocore, default is hostname", default=None)
    args = vars(parser.parse_args())
    return args


args = handleArgs()
# args = vars(parser.parse_args())
print(args)

mode = sys.argv[1]
if mode == 'bag':
    print("bag {} {}".format(args['mode'], args['filename']))
elif mode == 'topic':
    print("topic")
elif mode == 'multicast':
    print("multicast")
