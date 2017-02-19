#!/usr/bin/env python

# import sys
import threading
import time
from pygecko.lib import ZmqClass as Zmq
from pygecko.lib import Messages as Msg
from pygecko.lib.Topic import TopicPub
# import random
import zmq


def subscriber(msg):
	# Subscribe to everything
	sub = Zmq.Sub('test', connect_to=('localhost', 9000))

	# Get and process messages
	for i in range(7):
		tp, ret = sub.recv()
		if ret:
			assert ret == msg
			print 'found:', ret == msg
			return
		time.sleep(0.1)


def publisher(msg):
	# Prepare publisher
	pub = Zmq.Pub(bind_to=('localhost', 9000))

	for i in range(7):
		pub.pub('test', msg)
		time.sleep(0.1)


def test():
	msg = Msg.Vector()
	msg.set(1, 2, 3)

	pub_thread = threading.Thread(target=publisher, args=(msg,))
	pub_thread.daemon = True
	pub_thread.start()
	sub_thread = threading.Thread(target=subscriber, args=(msg,))
	sub_thread.daemon = True
	sub_thread.start()

	pub_thread.join()
	sub_thread.join()
	time.sleep(0.1)


# def topic(msg):
# 	# Subscribe to everything
# 	sub = Zmq.Sub('test', connect_to=('localhost', 9000))
#
# 	# Get and process messages
# 	for i in range(7):
# 		tp, ret = sub.recv()
# 		if ret:
# 			assert ret == msg
# 			print 'found:', ret == msg
# 			return
# 		time.sleep(0.1)
#
#
# def echo(msg):
# 	# Prepare publisher
# 	pub = Zmq.Pub(bind_to=('localhost', 9000))
#
# 	for i in range(7):
# 		pub.pub('test', msg)
# 		time.sleep(0.1)
#
#
# def test():
# 	msg = Msg.Vector()
# 	msg.set(1, 2, 3)
#
# 	pub_thread = threading.Thread(target=publisher, args=(msg,))
# 	pub_thread.daemon = True
# 	pub_thread.start()
# 	sub_thread = threading.Thread(target=subscriber, args=(msg,))
# 	sub_thread.daemon = True
# 	sub_thread.start()
#
# 	pub_thread.join()
# 	sub_thread.join()
# 	time.sleep(0.1)

if __name__ == '__main__':
	test()
