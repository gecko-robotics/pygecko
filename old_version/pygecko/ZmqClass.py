##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################
#
# Kevin J. Walchko 13 Oct 2014
#
# see http://zeromq.org for more info
# http://zguide.zeromq.org/py:all

from __future__ import print_function
from __future__ import division
import zmq
import simplejson as json
import socket as Socket
from .Messages import serialize, deserialize

"""
14.3.0
PyZMQ no longer calls Socket.close() or Context.term() during process cleanup.
Changes to garbage collection in Python 3.4 make this impossible to do sensibly.
"""


class ZMQError(Exception):
	pass


def zmq_version():
	"""
	What version of the zmq (C++) library is python tied to?
	"""
	print('Using ZeroMQ version: {0!s}'.format((zmq.zmq_version())))


class Base(object):
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
		print('Using ZeroMQ version: {0!s}'.format((zmq.zmq_version())))

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
	def __init__(self, bind_to=('0.0.0.0', 9000), hwm=100):
		Base.__init__(self)
		self.bind_to = self.getAddress(bind_to)

		try:
			self.socket = self.ctx.socket(zmq.PUB)
			self.socket.set_hwm(hwm)
			self.socket.bind(self.bind_to)
			# self.socket.setsockopt(zmq.SNDHWM, 1)

		except Exception as e:
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
		# self.socket.send_multipart([topic.encode('ascii'), jmsg.encode('ascii')])
		done = True
		while done:
			done = self.socket.send_multipart([topic, jmsg])
		# print('pub >>', topic.encode('ascii'))


"""
# http://zguide.zeromq.org/py:all

import zmq

# Prepare our context and sockets
context = zmq.Context()

# Connect to task ventilator
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")

# Connect to weather server
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://localhost:5556")
subscriber.setsockopt(zmq.SUBSCRIBE, b"10001")

# Initialize poll set
poller = zmq.Poller()
poller.register(receiver, zmq.POLLIN)
poller.register(subscriber, zmq.POLLIN)

# Process messages from both sockets
while True:
    try:
        socks = dict(poller.poll())
    except KeyboardInterrupt:
        break

    if receiver in socks:
        message = receiver.recv()
        # process task

    if subscriber in socks:
        message = subscriber.recv()
        # process weather update
"""


class Sub(Base):
	"""
	Simple subscriber
	"""
	def __init__(self, topics=None, connect_to=('0.0.0.0', 9000), poll_time=0.01, hwm=100):
		Base.__init__(self)
		self.connect_to = self.getAddress(connect_to)
		self.poll_time = poll_time

		if type(topics) is list:
			pass
		else:
			# raise Exception('topics must be a list')
			topics = [topics]

		self.topics = topics
		try:
			self.socket = self.ctx.socket(zmq.SUB)
			self.socket.set_hwm(hwm)  # set high water mark, so imagery doesn't buffer and slow things down
			self.socket.connect(self.connect_to)

			# manage subscriptions
			# can also use: self.socket.subscribe(topic) or unsubscribe()
			if topics is None:
				print("Receiving messages on ALL topics...")
				self.socket.setsockopt(zmq.SUBSCRIBE, b'')
			else:
				# print("{}:{} receiving messages on topics: {} ...".format(connect_to[0], connect_to[1], topics))
				for t in topics:
					print("{}:{} receiving messages on topics: {} ...".format(connect_to[0], connect_to[1], t))
					# self.socket.setsockopt(zmq.SUBSCRIBE, t.encode('ascii'))
					self.socket.setsockopt(zmq.SUBSCRIBE, t)

			self.poller = zmq.Poller()
			self.poller.register(self.socket, zmq.POLLIN)
# 			print('POLLER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

		except Exception as e:
			error = '[-] Sub Error, {0!s}'.format((str(e)))
			# print error
			raise ZMQError(error)

	def __del__(self):
		if self.topics is None:
			self.socket.setsockopt(zmq.UNSUBSCRIBE, b'')
		else:
			for t in self.topics:
				self.socket.setsockopt(zmq.UNSUBSCRIBE, t.encode('ascii'))
		self.socket.close()
		self._stop()

	def recv(self):
		# check to see if there is read, write, or erros
		r, w, e = zmq.select([self.socket], [], [], self.poll_time)

		topic = None
		msg = None

		if len(r) > 0:
			print('r', len(r))
			topic, jmsg = r[0].recv_multipart(flags=zmq.NOBLOCK)
			msg = deserialize(jmsg)
		if len(w) > 0:
			print('recv:: i see write socket events?')
		if len(e) > 0:
			print('recv:: i see error socket events?')

		return topic, msg

	# def recv(self):
	# 	# check to see if there is read, write, or erros
	#
	# 	topic = None
	# 	msg = None
	#
	# 	zmq.zmq_poll([(self.socket, zmq.POLLIN,)], 10)
	# 	socks = self.poller.poll(10)
	# 	print('socks', socks)
	# 	socks = dict(socks)
	# 	topic, jmsg = self.socket.recv_multipart()
	# 	print(topic)
	#
	# 	print('socks:', socks)
	#
	# 	cnt = 0
	# 	if socks.get(self.socket) == zmq.POLLIN:
	# 		print('pollin:')
	# 		try:
	# 			for i in range(10):
	# 				topic, jmsg = self.socket.recv_multipart()
	# 				msg = deserialize(jmsg)
	# 				cnt = i
	# 		except:
	# 			pass
	#
	# 		print('recv looped', cnt)
	# 	# print(topic, msg)
	#
	# 	return topic, msg


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
