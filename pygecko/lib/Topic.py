#!/usr/bin/env python
#
#
# copyright Kevin Walchko
#
# Basically a rostopic

from __future__ import division, print_function
import time
import logging
import multiprocessing as mp
from pygecko.lib import ZmqClass as Zmq


class TopicPub(mp.Process):
	def __init__(self, topic, msg, rate=1, port=9000):
		mp.Process.__init__(self)
		self.host = 'localhost'
		self.port = port
		self.topic = topic
		self.msg = msg
		self.rate = rate

		# logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger(__name__).addHandler(logging.NullHandler())

	def run(self):
		tcp = (self.host, self.port)
		pub = Zmq.Pub(tcp)
		msg = self.msg
		topic = self.topic
		dt = 1
		if self.rate != 0:
			dt = 1.0 / self.rate

		print('Pub[{}] @ {} Hz: {}'.format(topic, self.rate, msg))

		try:
			count = 0
			while True:
				count += 1
				pub.pub(topic, msg)
				if count % 100 == 0:
					print('Sent {} msgs'.format(count))
				# print '[>]', topic, ':', msg
				time.sleep(dt)  # 1/2 second sleep

		except (IOError, EOFError):
			self.logger.error('[-] Connection gone .... bye')
			return

		except KeyboardInterrupt:
			self.logger.info('[-] User hit Ctrl-C keyboard .... bye')
			return  # not cleanly exiting


class TopicSub(mp.Process):
	def __init__(self, host, port, topic):
		mp.Process.__init__(self)

		self.host = host
		self.port = port
		self.topic = topic
		# logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger(__name__).addHandler(logging.NullHandler())

	def run(self):
		tcp = (self.host, self.port)
		sub = Zmq.Sub(self.topic, tcp)

		try:
			while True:
				topic, msg = sub.recv()
				if msg: print('[<]', topic, ':', msg)

		except (IOError, EOFError):
			self.logger.info('[-] Connection gone .... bye')
			return
