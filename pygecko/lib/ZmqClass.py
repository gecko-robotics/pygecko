#!/usr/bin/env python
#
# Kevin J. Walchko 13 Oct 2014
#
# see http://zeromq.org for more info

from __future__ import print_function
from __future__ import division
import zmq
import simplejson as json
import socket as Socket
from Messages import serialize, deserialize


class ZMQError(Exception):
	pass


class Base(object):  # FIXME: 20160525 move printing statements to logging instead?
	"""
	Base class for other derived pub/sub/service classes
	"""
	def __init__(self):
		# functions
		self.ctx = zmq.Context()

		# self.poller = zmq.Poller()

	@staticmethod
	def zmq_version():
		"""
		What version of the zmq (C++) library is python tied to?
		"""
		print('Using ZeroMQ version: {0!s}'.format((zmq.version_info())))

	def _stop(self):
		"""
		Internal function, don't call
		"""
		self.ctx.term()
		addr = '(,)'
		if self.addr:
			addr = self.addr
		print('[<] shutting down {} for {}'.format(type(self).__name__, addr))

	def getAddress(self, hp):
		if hp[0] == 'localhost':  # do I need to do this?
			hp = (Socket.gethostbyname(Socket.gethostname()), hp[1])
		addr = 'tcp://{}:{}'.format(*hp)
		self.addr = addr
		return addr


class Pub(Base):
	"""
	Simple publisher
	"""
	def __init__(self, bind_to=('0.0.0.0', 9000), hwm=1):
		Base.__init__(self)
		self.bind_to = self.getAddress(bind_to)

		try:
			self.socket = self.ctx.socket(zmq.PUB)
			self.socket.set_hwm(hwm)
			self.socket.bind(self.bind_to)
			# self.socket.setsockopt(zmq.SNDHWM, 1)

		except Exception, e:
			error = '[-] Pub Error, {0!s}'.format((str(e)))
			# print error
			raise ZMQError(error)

		# self.poller.register(self.socket, zmq.POLLOUT)

	def __del__(self):
		# self.poller.register(self.socket)
		self.socket.close()
		self._stop()

	def pub(self, topic, msg):
		"""
		It appears the send_json() doesn't work for pub/sub.
		in: topic, message
		out: none
		"""
		jmsg = serialize(msg)
		self.socket.send_multipart([topic, jmsg])


class Sub(Base):
	"""
	Simple subscriber
	"""
	def __init__(self, topics=None, connect_to=('0.0.0.0', 9000), poll_time=0.01, hwm=1):
		Base.__init__(self)
		self.connect_to = self.getAddress(connect_to)
		self.poll_time = poll_time
		self.topics = topics
		try:
			self.socket = self.ctx.socket(zmq.SUB)
			self.socket.set_hwm(hwm)  # set high water mark, so imagery doesn't buffer and slow things down
			self.socket.connect(self.connect_to)
			self.socket.poll(self.poll_time, zmq.POLLIN)

			# manage subscriptions
			# can also use: self.socket.subscribe(topic) or unsubscribe()
			if topics is None:
				print("Receiving messages on ALL topics...")
				self.socket.setsockopt(zmq.SUBSCRIBE, '')
			else:
				print("{}:{} receiving messages on topics: {} ...".format(connect_to[0], connect_to[1], topics))
				for t in topics:
					self.socket.setsockopt(zmq.SUBSCRIBE, t)

		except Exception, e:
			error = '[-] Sub Error, {0!s}'.format((str(e)))
			# print error
			raise ZMQError(error)

	def __del__(self):
		if self.topics is None:
			self.socket.setsockopt(zmq.UNSUBSCRIBE, '')
		else:
			for t in self.topics:
				self.socket.setsockopt(zmq.UNSUBSCRIBE, t)
		self.socket.close()
		self._stop()

	def recv(self):
		# check to see if there is read, write, or erros
		r, w, e = zmq.select([self.socket], [], [], self.poll_time)

		topic = None
		msg = None

		# should this be a for loop? I don't think so???
		if len(r) > 0:
			topic, jmsg = r[0].recv_multipart()
			# import sys
			# print(sys.getsizeof(jmsg))
			# msg = json.loads(jmsg)
			msg = deserialize(jmsg)
		return topic, msg


class ServiceProvider(Base):
	"""
	Provides a service
	"""
	def __init__(self, bind_to):
		Base.__init__(self)
		self.socket = self.ctx.socket(zmq.REP)
		# tcp = 'tcp://' + bind_to[0] + ':' + str(bind_to[1])
		tcp = self.getAddress(bind_to)
		self.socket.bind(tcp)

	def __del__(self):
		self.socket.close()
		self._stop()

	def listen(self, callback):
		# print 'listen'
		while True:
			jmsg = self.socket.recv()
			msg = json.loads(jmsg)

			ans = callback(msg)

			jmsg = json.dumps(ans)
			self.socket.send(jmsg)


class ServiceClient(Base):
	"""
	Client socket to get a response back from a service provider
	"""
	def __init__(self, bind_to):
		Base.__init__(self)
		self.socket = self.ctx.socket(zmq.REQ)
		# tcp = 'tcp://' + bind_to[0] + ':' + str(bind_to[1])
		tcp = self.getAddress(bind_to)
		self.socket.connect(tcp)

	def __del__(self):
		self.socket.close()
		self._stop()

	def get(self, msg):
		jmsg = json.dumps(msg)
		self.socket.send(jmsg)
		jmsg = self.socket.recv()
		msg = json.loads(jmsg)
		return msg


# if __name__ == "__main__":
# 	print('hello cowboy!')
