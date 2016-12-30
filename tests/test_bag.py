#!/usr/bin/env python

import os
import sys
# sys.path.insert(0, os.path.abspath('..'))
from pygecko.lib.Bag import Bag
import pygecko.lib.Messages as Msg
import random


def test_bag():
	bag = Bag()
	bag.open('imu')

	num_msg = 105

	for i in range(0, num_msg):
		msg = Msg.Vector()
		msg.update({'x': random.uniform(-3, 3), 'y': random.uniform(10, 50), 'z': random.uniform(-20, 5)})
		bag.push(msg)
	bag.close()

	filename = 'imu.bag'
	ans = bag.readFromFile(filename)
	os.remove(filename)
	# print 'Found {} messages in file {}'.format(len(ans), filename)
	# print 'type:', type(ans[0])
	# print ans[0]
	assert len(ans) == num_msg and isinstance(ans[0], dict)