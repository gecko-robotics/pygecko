import numpy as np
from pygecko import ZmqClass as zmq
from pygecko.Messages import Image, Vector, dict_to_class
# from pygecko.lib.Messages import serialize, deserialize
# import simplejson as json
from pygecko import Messages as Msgs


def test_pub_sub():
	tcp = ('127.0.0.1', 9000)
	pub = zmq.Pub(tcp)
	sub = zmq.Sub(['test'], tcp)
	# tmsg = {'a': 1, 'b': 2}
	tmsg = Vector()
	tmsg.set(2, 3, 4)
	while True:
		pub.pub('test', tmsg)
		topic, msg = sub.recv()

		if msg:
			assert msg == tmsg
			assert topic == b'test'
			break


def test_pub_sub_msgs():
	tcp = ('127.0.0.1', 9001)
	pub = zmq.Pub(tcp)
	sub = zmq.Sub(['test'], tcp)
	msgs = [
		Msgs.Vector(),
		Msgs.Quaternion(),
		Msgs.Array(),
		Msgs.IMU(),
		Msgs.Dictionary(),
		Msgs.Odom(),
		Msgs.Joystick(),
		Msgs.Twist(),
		Msgs.Wrench()
	]
	for tmsg in msgs:
		while True:
			print(tmsg)
			pub.pub('test', tmsg)
			topic, msg = sub.recv()

			if msg:
				assert msg == tmsg
				assert topic == b'test'
				break


def test_pub_sub_vector():
	tcp = ('127.0.0.1', 9001)
	pub = zmq.Pub(tcp)
	sub = zmq.Sub(['test'], tcp)
	d = {'Class': 'Vector', 'x': 1.0, 'z': 2.0}
	tmsg = dict_to_class(d)
	for _ in range(10):
		pub.pub('test', tmsg)
		topic, msg = sub.recv()

		if msg:
			assert msg == tmsg
			assert topic == b'test'
			# break


def test_pub_sub_b64():
	tcp = ('127.0.0.1', 9002)
	pub = zmq.Pub(tcp)
	sub = zmq.Sub(['test'], tcp)
	im = np.random.rand(100, 100)
	tmsg = Image()
	tmsg.img = im
	# print(tmsg['size'], tmsg['depth'])
	while True:
		pub.pub('test', tmsg)
		topic, msg = sub.recv()

		print('topic?', topic)

		if msg:
			if tmsg.b64:
				tmsg.decodeB64()
			assert msg.img.shape == tmsg.img.shape
			assert msg.img.all() == tmsg.img.all()
			assert topic == b'test'
			break


# def test_serivce():
#
# 	ans = {'a': 1, 'b': 2}
#
# 	class tServer(mp.Process):
# 		def __init__(self):
# 			mp.Process.__init__(self)
#
# 		def run(self):
# 			tcp = ('127.0.0.1', 9000)
# 			serv = zmq.ServiceProvider(tcp)
# 			serv.listen(self.callback)
# 			return 0
#
# 		def callback(self, msg):
# 			return msg
#
# 	s = tServer()
# 	s.start()
#
# 	tcp = ('127.0.0.1', 9000)
# 	client = zmq.ServiceClient(tcp)
# 	msg = client.get(ans)
# 	assert msg == ans
#
# 	s.terminate()
# 	s.join()
