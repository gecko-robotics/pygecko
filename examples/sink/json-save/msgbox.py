#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2014 Kevin Walchko
# see LICENSE for full details
##############################################
#

try:
    import simplejson as json
except ImportError:
    import json


# class MsgBox(object):
#     def __init__(self, fname, buffer_size=500):
#         self.fd = open(fname, 'w')
#         self.buffer = {}
#         self.buffer_size = buffer_size
#         self.counter = 0
#
#     def __del__(self):
#         if self.counter > 0:
#             self.write()
#         self.close()
#
#     def push(self, topic, data):
#         # self.buffer.append(data)
#         # if topic not in self.buffer:
#         try:
#             self.buffer[topic].append(data)
#         except KeyError:
#             self.buffer[topic] = []
#             self.buffer[topic].append(data)
#
#         # self.buffer[topic].append(data)
#         self.counter += 1
#         if self.counter > self.buffer_size:
#             self.write()
#
#     def write(self):
#         print('>> write', self.buffer)
#         json.dump(self.buffer, self.fd)
#         self.buffer = {}
#         self.counter = 0
#         if self.fd.closed:
#             print("file closed")
#
#     def close(self):
#         if self.counter > 0:
#             self.write()
#         if not self.fd.closed:
#             self.fd.close()
#
#     @staticmethod
#     def read(fname):
#         data = {}
#         try:
#             fd = open(fname, "r")
#             while True:
#                 d = json.load(fd)
#                 for k, v in d.items():
#                     try:
#                         data[k] += v
#                     except KeyError:
#                         data[k] = []
#                         data[k] += v
#                 print('>> read', d)
#         except EOFError:
#             pass
#         return data
