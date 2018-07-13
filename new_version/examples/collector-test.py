#!/usr/bin/env python3

from __future__ import print_function, division
from the_collector import BagReader, BagWriter

# fix path for now
import sys
sys.path.append("../")
from pygecko.transport.messages import serialize
from pygecko.transport.messages import deserialize
from pygecko.transport.messages import Vector
from pygecko.transport.messages import IMU


if __name__ == '__main__':
    # bag files store data for us
    bag = BagWriter(pack=serialize)

    # save a copy of the data for comparison
    save = {
        'vector': [],
        'imu': []
    }

    # push data into bag
    for i in range(100):
        v = Vector(i, i/20, i/100)
        bag.push('vector', v)
        save['vector'].append(v)
        imu = IMU(Vector(1, 1, 1), Vector(2, 2, 2), Vector(3, 3, 3))
        bag.push('imu', imu)
        save['imu'].append(imu)

    # save the bag file
    bag.write('test.bag')

    # open the bag and read back the data
    bag = BagReader(unpack=deserialize)
    data = bag.read('test.bag')

    # does it match????
    print('Data match?', data == save)
