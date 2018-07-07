#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import msgpack
from collections import namedtuple
import time


# fix path for now
import sys
sys.path.append("../")

from pygecko.transport.messages import *

# class TimeStamp(object):
#     def get(self):
#         return time.time()
#     def format(self, ts):
#         return "fix me"

"""
idc = {
	'Image': Image,
	'Vector': Vector,
	'Quaternion': Quaternion,
	'Wrench': Wrench,
	'Pose': Pose,
	'Twist': Twist,
	'IMU': IMU,
	'Odom': Odom,
	'Axes': Axes,
	'Buttons': Buttons,
	'Joystick': Joystick,
	'Compass': Compass,
	'Range': Range,
	'Power': Power,
	'Array': Array,
	'Dictionary': Dictionary
}
"""

def makets():
    """
    returns a timestamp
    """
    return time.time()

def formatts(ts):
    return "fixme"

# # simple ones, no stamp, wouldn't just send these. They are datatypes that
# # get put into a messagel
# #
# # cant do: func(*Vector); you would pass in timestamp too!
# # but you could do: func(Vector[:3]); cut off stamp
# Vector = namedtuple('Vector', 'x y z')
# Quaternion = namedtuple('Quaternion', 'w x y z')
#
# """
# d = img.tobytes()
# s = img.shape
# msg = Image(s, d, makets())
#
# img = np.frombytes(msg.d, dtype=np.uint8)
# img.reshape(msg.shape)
# """
#
# # with timestamp
# Image = namedtuple('Image', 'shape data timestamp')
# Lidar = namedtuple('Lidar', 'len data timestamp')
Pose = namedtuple('Pose', 'position orientation timestamp')
IMU = namedtuple('IMU', 'linear_accel angular_vel magnetic_field timestamp')
# Path = namedtuple("Path", 'path')


a = (1, 2, 3)
g = (1, 2, 3)
m = (1, 2, 3)
IMU(Vector(*a), Vector(*g), Vector(*m), makets())

Pose(Vector(1, 2, 3), Quaternion(1, 0, 0, 0), makets())


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
        10: Pose(Vector(1, 2, 3), Quaternion(1, 2, 3, 4), makets()),
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
