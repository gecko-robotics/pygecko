#!/usr/bin/env python


import numpy as np
import multiprocessing as mp
import pygecko.lib.ZmqClass as zmq
from pygecko.lib.Messages import Image


def test_pub_sub():
	tcp = ('127.0.0.1', 9000)
	pub = zmq.Pub(tcp)
	sub = zmq.Sub('test', tcp)
	tmsg = {'a': 1, 'b': 2}
	while True:
		pub.pub('test', tmsg)
		topic, msg = sub.recv()

		if msg:
			assert msg == tmsg
			assert topic == 'test'
			break


def test_pub_sub_b64():
	tcp = ('127.0.0.1', 9000)
	pub = zmq.Pub(tcp)
	sub = zmq.Sub('test', tcp)
	im = np.random.rand(100, 100)
	tmsg = Image(im)
	# print(tmsg['size'], tmsg['depth'])
	while True:
		pub.pubB64('test', tmsg)
		topic, msg = sub.recvB64()

		if msg:
			# print(msg['size'], msg['depth'])
			assert msg['size'] == tmsg['size']
			assert msg['depth'] == tmsg['depth']
			assert topic == 'test'
			break


def test_serivce():

	ans = {'a': 1, 'b': 2}

	class tServer(mp.Process):
		def __init__(self):
			mp.Process.__init__(self)

		def run(self):
			tcp = ('127.0.0.1', 9000)
			serv = zmq.ServiceProvider(tcp)
			serv.listen(self.callback)
			return 0

		def callback(self, msg):
			return msg

	s = tServer()
	s.start()

	tcp = ('127.0.0.1', 9000)
	client = zmq.ServiceClient(tcp)
	msg = client.get(ans)
	assert msg == ans

	s.terminate()
	s.join()
