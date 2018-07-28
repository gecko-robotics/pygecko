# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# from __future__ import print_function
# import msgpack
# from collections import namedtuple
# import time
#
#
# # fix path for now
# import sys
# sys.path.append("../")
#
# from the_collector.messages import *
#
# # class TimeStamp(object):
# #     def get(self):
# #         return time.time()
# #     def format(self, ts):
# #         return "fix me"
#
# def makets():
#     """
#     returns a timestamp
#     """
#     return time.time()
#
# def formatts(ts):
#     return "fixme"
#
# # # simple ones, no stamp, wouldn't just send these. They are datatypes that
# # # get put into a messagel
# # #
# # # cant do: func(*Vector); you would pass in timestamp too!
# # # but you could do: func(Vector[:3]); cut off stamp
# # Vector = namedtuple('Vector', 'x y z')
# # Quaternion = namedtuple('Quaternion', 'w x y z')
# #
# # """
# # d = img.tobytes()
# # s = img.shape
# # msg = Image(s, d, makets())
# #
# # img = np.frombytes(msg.d, dtype=np.uint8)
# # img.reshape(msg.shape)
# # """
# #
# # # with timestamp
# # Image = namedtuple('Image', 'shape data timestamp')
# # Lidar = namedtuple('Lidar', 'len data timestamp')
# # Pose = namedtuple('Pose', 'position orientation timestamp')
# # IMU = namedtuple('IMU', 'linear_accel angular_vel magnetic_field timestamp')
# # Path = namedtuple("Path", 'path')
#
#
# a = (1, 2, 3)
# g = (1, 2, 3)
# m = (1, 2, 3)
# IMU(Vector(*a), Vector(*g), Vector(*m))
#
# Pose(Vector(1, 2, 3), Quaternion(1, 0, 0, 0), makets())
#
#
# # if i use this: use_list=False
# # then do i change the below to a tuple?
# # def ext_pack(x):
# #     if x.__class__.__name__ in ['Quaternion', 'Vector', 'Pose', 'Image', 'Lidar']:
# #         return msgpack.ExtType(1, msgpack.packb([x.__class__.__name__,] + list(x[:]), default=ext_pack, strict_types=True))
# #     return x
# #
# # def ext_unpack(code, data):
# #     if code == 1:
# #         # you call this again to unpack and ext_hook for nested
# #         d = msgpack.unpackb(data, ext_hook=ext_unpack, raw=False)
# #
# #         # print d[0]   # holds class name
# #         # print d[1:]  # holds data inorder
# #         # finds constructor in namespace and calls it
# #         return globals()[d[0]](*d[1:])
# #     return msgpack.ExtType(code, data)
#
#
# # Define data
# data = {'a list': [1, 42, 3.141, 1337, 'help'],
#         'a string': 'bla',
#         # 6: bytearray(range(255))*1000,
#         8: Vector(1.22, 3.44, 5.66),
#         9: Quaternion(1, 2, 3, 4),
#         10: Pose(Vector(1, 2, 3), Quaternion(1, 2, 3, 4)),
#         11: IMU(Vector(*a), Vector(*g), Vector(*m)),
#         'another dict': {'foo': 'bar',
#                          'key': 'value',
#                          'the answer': 42}}
#
# print('Starting msg ------------------------')
# for k in data.keys():
#     print('  ', data[k])
# print('-------------------------------------')
#
# filename = 'data3.msgpack'
#
#
# # Write msgpack file
# def writeout(filename, data):
#     with open(filename, 'w') as outfile:
#         msgpack.pack(data, outfile, default=serialize, strict_types=True, use_bin_type=True)
#
#
# # Read msgpack file
# def readin(filename):
#     with open(filename) as data_file:
#         data_loaded = msgpack.unpack(data_file, ext_hook=deserialize, raw=False)
#     return data_loaded
#
#
# d = [data for _ in range(1000)]
#
#
# writeout(filename, d)
# data_loaded = readin(filename)
#
# print('Does data match?', d == data_loaded)
#
# print('Ending msg ------------------------')
# for k in data_loaded[0].keys():
#     print('  ', data_loaded[0][k])
# print('-------------------------------------\n')
# # for a, b in zip(data)
# # print(data)
# # print(data_loaded)
