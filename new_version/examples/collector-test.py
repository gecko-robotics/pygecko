#!/usr/bin/env python

from __future__ import print_function, division
# import multiprocessing as mp
# import time
from the_collector import BagReader, BagWriter

# fix path for now
import sys
sys.path.append("../")

# from pygecko.transport import Pub, Sub
# from pygecko.transport import zmqTCP, GeckoCore
from pygecko.transport.messages import serialize, deserialize, Vector


if __name__ == '__main__':
    bag = BagWriter(pack=serialize)

    for i in range(100):
        v = Vector(i, i/20, i/100)
        bag.push(v)

    bag.write('test.bag')

    bag = BagReader(unpack=deserialize)
    data = bag.read('test.bag')

    for d in data:
        print(d)
