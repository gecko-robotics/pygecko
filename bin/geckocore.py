#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2014 Kevin Walchko
# see LICENSE for full details
##############################################
# import time
# from pygecko.transport import GeckoCore
#
#
# if __name__ == "__main__":
#     core = GeckoCore()
#     core.start()
#
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         pass
# import threading
# import time
import argparse
import socket
from pygecko.pycore.mbeacon import BeaconCoreServer
from pygecko.pycore.transport import Ascii


def handleArgs():
    parser = argparse.ArgumentParser(description='geckocore is a conneciton server for gecko apps')
    # parser.add_argument('file', help='launch file')
    # parser.add_argument('-f', '--format', help='format: json or yaml, default is json', default='json')
    parser.add_argument('-k', '--key', help="key for the geckocore, default is hostname", default=None)
    args = vars(parser.parse_args())
    return args


if __name__ == "__main__":
    args = handleArgs()

    if args['key'] is None:
        key = socket.gethostname().lower().split('.')[0]
    else:
        key = args['key']

    bs = BeaconCoreServer(key=key, handler=Ascii)
    bs.start()
    bs.run()
