#!/usr/bin/env python

from __future__ import print_function
from pygecko import ZmqClass as zmq
from pygecko import Messages as Msg
import time
# import sys
# import random
from multiprocessing import Process


def Pub():
	pub = zmq.Pub(('127.0.0.1', 9000))
	print('start pub')
	cnt = 0
	while True:
		# msg = Msg.Array()
		# msg.append(1)
		# msg.append(2)
		msg = Msg.Vector()
		cnt += 1
		msg.set(1, 2, cnt)
		pub.pub('a', msg)
		# print('>>', msg)

		msg = Msg.Dictionary()
		msg.dict['bob'] = 1
		pub.pub('b', msg)
		# print('>>', msg)
		time.sleep(.1)


def Sub():
	sub = zmq.Sub(['a', 'b'], ('127.0.0.1', 9000))
	print('start sub')
	while True:
		topic, msg = sub.recv()
		print('<<', topic, msg)
		time.sleep(2)


if __name__ == '__main__':
	try:
		p = Process(target=Pub).start()
		s = Process(target=Sub).start()
		p.join()
		s.join()
	except KeyboardInterrupt:
		# p.join()
		# s.join()
		if p.is_alive():
			p.terminate()
		if s.is_alive():
			s.terminate()
