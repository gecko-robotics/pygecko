#!/usr/bin/env python

from pygecko import ZmqClass as zmq
from pygecko import Messages as Msg
import time
# import sys
# import random
from multiprocessing import Process


class tPub(Process):
	def __init__(self):
		# Process.__init__(self)
		super(tPub, self).__init__()
		# self.daemon = True
		self.pub = zmq.Pub(('127.0.0.1', 9000))

	def run(self):
		print('start pub')
		while True:
			# msg = Msg.Array()
			# msg.append(1)
			# msg.append(2)
			msg = Msg.Vector()
			msg.set(1, 2, 3)
			self.pub.pub('a', msg)
			print(msg)

			msg = Msg.Dictionary()
			msg.dict['bob'] = 1
			self.pub.pub('b', msg)
			print(msg)
			time.sleep(1)


class tSub(object):
	def __init__(self):
		# Process.__init__(self)
		# self.sub = zmq.Sub(['a', 'b'], ('127.0.0.1', 9000))
		self.sub = zmq.Sub(['a'], ('127.0.0.1', 9000))

	def start(self):
		print('start sub')
		while True:
			topic, msg = self.sub.recv()
			print(' >>', topic, msg)
			time.sleep(1.5)


if __name__ == '__main__':
	p = tPub()
	# s = tSub()

	try:
		p.start()
		# s.start()
		p.join()

	except KeyboardInterrupt:
		# s.join()
		# s.terminate()
		p.terminate()
