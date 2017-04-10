#!/usr/bin/env python

from __future__ import print_function
import multiprocessing as mp
import time
# import random
import zmq
import sys
import itertools
import json

PY = sys.version_info[:3]

if PY[0] == 3:
	from zmq.utils.strtypes import asbytes

print('Using python: {}'.format(PY))
topics = [b'speed', b'acceleration', b'mass']


def subscriber(msg):
	# Subscribe to everything
	ctx = zmq.Context.instance()
	sub = ctx.socket(zmq.SUB)
	sub.setsockopt(zmq.SUBSCRIBE, b'')
	# sub.setsockopt(zmq.SUBSCRIBE, [b'speed', b'mass'])

	sub.connect("tcp://localhost:5556")

	# Get and process messages
	while True:
		try:
			tp, msg = sub.recv_multipart()
			msg = json.loads(msg)
			print('recvd:', tp, msg)
		except Exception:
			pass

		time.sleep(1)


def publisher(in_msg):
	# Prepare publisher
	ctx = zmq.Context.instance()
	pub = ctx.socket(zmq.PUB)
	pub.bind("tcp://*:5556")

	for topic in itertools.cycle(topics):
		msg = in_msg
		msg['time'] = str(time.time())

		msg = json.dumps(msg)
		if PY[0] == 3:
			msg = asbytes(msg)

		pub.send_multipart([topic, msg])
		time.sleep(1e-3)            # 1msec wait


def main():
	msg = {'a': 1}

	mpub = mp.Process(name='pub', target=publisher, args=(msg,))
	msub = mp.Process(name='sub', target=subscriber, args=(msg,))

	mpub.start()
	msub.start()


if __name__ == '__main__':
	main()
