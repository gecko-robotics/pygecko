#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2014 Kevin Walchko
# see LICENSE for full details
##############################################
#

# from pygecko.multiprocessing import geckopy
import pickle


class PickleJar(object):
    def __init__(self, fname, buffer_size=500):
        ext = fname.split('.')[-1]
        if ext != 'pickle':
            fname += '.pickle'
        self.fd = open(fname, 'wb')
        self.buffer = {}
        self.buffer_size = buffer_size
        self.counter = 0

    def __del__(self):
        if self.counter > 0:
            self.write()
        self.close()

    def push(self, topic, data):
        # self.buffer.append(data)
        # if topic not in self.buffer:
        try:
            self.buffer[topic].append(data)
        except KeyError:
            self.buffer[topic] = []
            self.buffer[topic].append(data)

        # self.buffer[topic].append(data)
        self.counter += 1
        if self.counter > self.buffer_size:
            self.write()

    def write(self):
        # print('>> write', self.buffer)
        pickle.dump(self.buffer, self.fd)
        self.buffer = {}
        self.counter = 0
        # if self.fd.closed:
        #     print("file closed")

    def close(self):
        if self.counter > 0:
            self.write()
        if not self.fd.closed:
            self.fd.close()

    @staticmethod
    def read(fname):
        data = {}
        try:
            fd = open(fname, "rb")
            while True:
                d = pickle.load(fd)
                for k, v in d.items():
                    try:
                        data[k] += v
                    except KeyError:
                        data[k] = []
                        data[k] += v
                # print('>> read', d)
        except EOFError:
            pass
        except FileNotFoundError as e:
            print(e)
            data = None
        return data
