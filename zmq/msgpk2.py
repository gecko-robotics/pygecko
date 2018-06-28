#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import msgpack
from collections import namedtuple

Vector = namedtuple('Vector', 'x y z')
Quaternion = namedtuple('Quaternion', 'w x y z')
Pose = namedtuple('Pose', 'p o')
Image = namedtuple('Image', 'shape data')
Lidar = namedtuple('Lidar', 'len data')

"""
>>> v = Vector(1,2,3)
>>> v.__class__.__name__
'Vector'
"""

# if i use this: use_list=False
# then do i change the below to a tuple?
def ext_pack(x):
    if x.__class__.__name__ in ['Quaternion', 'Vector', 'Pose', 'Image', 'Lidar']:
        return msgpack.ExtType(1, msgpack.packb([x.__class__.__name__,] + list(x[:]), default=ext_pack, strict_types=True))
    return x

def ext_unpack(code, data):
    if code == 1:
        # you call this again to unpack and ext_hook for nested
        d = msgpack.unpackb(data, ext_hook=ext_unpack, raw=False)

        # print d[0]   # holds class name
        # print d[1:]  # holds data inorder
        # finds constructor in namespace and calls it
        return globals()[d[0]](*d[1:])
    return msgpack.ExtType(code, data)


# Define data
data = {'a list': [1, 42, 3.141, 1337, 'help'],
        'a string': 'bla',
        # 6: bytearray(range(255))*1000,
        8: Vector(1.22, 3.44, 5.66),
        9: Quaternion(1, 2, 3, 4),
        10: Pose(Vector(1, 2, 3), Quaternion(1, 2, 3, 4)),
        'another dict': {'foo': 'bar',
                         'key': 'value',
                         'the answer': 42}}


filename = 'data3.msgpack'


# Write msgpack file
def writeout(filename, data):
    with open(filename, 'w') as outfile:
        msgpack.pack(data, outfile, default=ext_pack, strict_types=True, use_bin_type=True)


# Read msgpack file
def readin(filename):
    with open(filename) as data_file:
        # data_loaded = json.load(data_file)
        data_loaded = msgpack.unpack(data_file, ext_hook=ext_unpack, raw=False)
    return data_loaded


d = [data for _ in range(1000)]


writeout(filename, d)
data_loaded = readin(filename)

print(d == data_loaded)
# for a, b in zip(data)
# print(data)
# print(data_loaded)
