#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################
import time
import argparse
import os
from pygecko.transport.beacon import BeaconFinder


def handleArgs():
    parser = argparse.ArgumentParser(description='Use multicast to find a geckocore node on the network')
    parser.add_argument('-k', '--key', help='key, default is hostname', default=None)
    args = vars(parser.parse_args())
    return args


if __name__ == "__main__":
    args = handleArgs()
    key = args['key']
    if key is None:
        key = os.uname().nodename.split('.')[0].lower()
    finder = BeaconFinder(key)
    resp = finder.search(0,"0")
    if resp:
        print("[GeckoCore]===========================")
        print("   in: {}".format(resp[0]))
        print("  out: {}".format(resp[1]))
    else:
        print("*** No GeckoCore found on this network ***")
