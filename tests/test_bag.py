#!/usr/bin/env python

import os
from pygecko import Bag
import pygecko.Messages as Msg
# import random


def test_bag():
	bag = Bag()
	bag.open('imu')

	num_msg = 105

	for i in range(0, num_msg):
		msg = Msg.Vector()
		msg.set(1, 2, 3)
		bag.push(msg)
	bag.close()

	filename = 'imu.bag'
	ans = bag.readFromFile(filename)
	os.remove(filename)
	# print 'Found {} messages in file {}'.format(len(ans), filename)
	# print 'type:', type(ans[0])
	# print ans[0]
	assert len(ans) == num_msg
	assert isinstance(ans[0], Msg.Vector)
