#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

from pygecko.multiprocessing import geckopy
from pygecko.multiprocessing import GeckoSimpleProcess
import pickle

class PickleJar(object):
    def __init__(self, fname, buffer_size=100):
        self.fd = open(fname, 'wb')
        self.buffer = []
        self.buffer_size = buffer_size
    def __del__(self):
        self.close()
    def push(self, data):
        self.buffer.append(data)
        if len(self.buffer) > self.buffer_size:
            self.write()
    def write(self):
        for d in self.buffer:
            pickle.dump(d, self.fd)
        self.buffer = []
    def close(self):
        self.fd.close()


class Callback(object):
    def __init__(self):
        self.jar = PickleJar('test.pickle')
    def callback(self, topic, msg):
        geckopy.loginfo("recv[{}]: {}".format(topic, msg))
        self.jar.push(msg)

def subscriber(**kwargs):
    geckopy.init_node(**kwargs)
    c = Callback()
    geckopy.Subscriber(['data'], c.callback)

    geckopy.spin(2) # it defaults to 100hz, this is just to slow it down
    print('sub bye ...')


def publisher(**kwargs):
    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(1)

    p = geckopy.Publisher()

    while not geckopy.is_shutdown():
        msg = {'a': 1}
        p.pub('data', msg)
        rate.sleep()

    print('pub bye ...')


if __name__ == '__main__':
    args = {}
    p = GeckoSimpleProcess()
    p.start(func=publisher, name='publisher', kwargs=args)

    s = GeckoSimpleProcess()
    s.start(func=subscriber, name='subscriber', kwargs=args)
