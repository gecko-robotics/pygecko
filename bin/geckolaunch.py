#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2014 Kevin Walchko
# see LICENSE for full details
##############################################

"""
So this is sort of a copy of roslaunch
needs to move to bin
"""

import argparse
from pygecko.multiprocessing import GeckoLauncher
from pygecko.file_storage import FileYaml
from pygecko.file_storage import FileJson

# https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes

def handleArgs():
    parser = argparse.ArgumentParser(description='Launches multiple programs')
    parser.add_argument('file', help='launch file')
    parser.add_argument('-f', '--format', help='format: json or yaml, default is json', default='json')
    args = vars(parser.parse_args())
    return args

if __name__ == '__main__':
    args = handleArgs()

    # get extension to determine if it is a yaml or json file
    fname = args['file']
    ext = fname.split('.')[-1]  # there could be . in the filename, so grab end

    if args['format'] == 'json':
        if ext != 'json':
            print("Expected a json file: {}".format(fname))
            exit(1)
        reader = FileJson()

    elif args['format'] == 'yaml':
        if ext not in ['yaml','yml']:
            print("Expected a yaml file: {}".format(fname))
            exit(1)
        reader = FileYaml()

    try:
        ps = reader.read(fname)
    except Exception as e:
        print(e)
        exit(1)

    # print(ps)

    g = GeckoLauncher(ps)
    g.loop()
