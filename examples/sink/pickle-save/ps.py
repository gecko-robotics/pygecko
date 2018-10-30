#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
from picklesave import PickleJar
from pygecko.multiprocessing import geckopy
from pygecko.multiprocessing import GeckoSimpleProcess
from pygecko import IMU, Vector
import pickle
from pprint import pprint


def subscriber(**kwargs):
    geckopy.init_node(**kwargs)
    c = Callback()
    geckopy.Subscriber(['data'], c.callback)

    geckopy.spin(2) # it defaults to 100hz, this is just to slow it down
    print('sub bye ...')


def publisher(**kwargs):
    geckopy.init_node(**kwargs)
    rate = geckopy.Rate(1)

    p = geckopy.Publisher(['data'])

    while not geckopy.is_shutdown():
        msg = {'a': 1}
        p.pub('data', msg)
        rate.sleep()

    print('pub bye ...')


if __name__ == '__main__':
    jar = PickleJar("t.pickle", buffer_size=5)
    # jar = MsgBox("t.p", buffer_size=5)
    names = ['a','b','c']
    for i in range(30):
        msg = IMU(Vector(1,2,3), Vector(4,5,6), Vector(7,8,9))
        jar.push(names[i%3], msg)

    jar.close()

    print("\n=======================\n")

    data = PickleJar.read("t.pickle")
    # data = MsgBox.read("t.pickle")

    print("\n=======================\n")

    if data:
        for key in data:
            print('\n[{}]--------'.format(key))
            for d in data[key]:
                print('  {}'.format(d))

    # with open("t.p", "rb") as fd:
    #     d = pickle.load(fd)
    #     print(d)

    # print(d)
    # args = {}
    # p = GeckoSimpleProcess()
    # p.start(func=publisher, name='publisher', kwargs=args)
    #
    # s = GeckoSimpleProcess()
    # s.start(func=subscriber, name='subscriber', kwargs=args)
