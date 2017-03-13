#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################
import time
import simplejson as json  # supposed to be better than json
import math
import numpy as np
import base64
import cv2
from functools import wraps
# import time


class MessageError(Exception):
	pass


# http://stackoverflow.com/questions/3603502/prevent-creating-new-attributes-outside-init
def froze_it(cls):
	cls.__frozen = False

	def frozensetattr(self, key, value):
		if self.__frozen and not hasattr(self, key):
			# print("Class {} is frozen. Cannot set {} = {}".format(cls.__name__, key, value))
			raise MessageError("Class {} is frozen. Cannot set {} = {}".format(cls.__name__, key, value))
		else:
			object.__setattr__(self, key, value)

	def init_decorator(func):
		@wraps(func)
		def wrapper(self, *args, **kwargs):
			func(self, *args, **kwargs)
			self.__frozen = True
		return wrapper

	cls.__setattr__ = frozensetattr
	cls.__init__ = init_decorator(cls.__init__)

	return cls


@froze_it
class Vector(object):
	def __init__(self, data=None):
		self.Class = 'Vector'
		self.x = 0
		self.y = 0
		self.z = 0
		if data:
			for key in data:
				setattr(self, key, data[key])

	def set(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def __str__(self):
		s = 'x: {:.2f} y: {:.2f} z: {:.2f}'.format(self.x, self.y, self.z)
		return s

	def __eq__(self, v):
		return (self.x == v.x and self.y == v.y and self.z == v.z)


@froze_it
class Quaternion(object):
	def __init__(self, data=None):
		self.Class = 'Quaternion'
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
		self.w = 1.0
		if data:
			for key in data:
				setattr(self, key, data[key])

	def normalize(self):
		d = math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
		if d > 0.0:
			self.x /= d
			self.y /= d
			self.z /= d
			self.w /= d

	def set(self, w, x, y, z):
		self.w = w
		self.x = x
		self.y = y
		self.z = z

	def __str__(self):
		s = 'w: {:.3f} x: {:.3f} y: {:.3f} z: {:.3f}'.format(self.w, self.x, self.y, self.z)
		return s

	def __eq__(self, q):
		return (self.x == q.x and self.y == q.y and self.z == q.z and self.w == q.w)


@froze_it
class Compass(object):
	"""
	Simple tilt compensated compass message, the roll, pitch, and heading angles
	are stored either in radians or degrees.
	"""
	COMPASS_RADIANS = 0
	COMPASS_DEGREES = 1
	kind = {
		0: 'Rads',
		1: 'Deg'
	}

	def __init__(self, data=None, units=COMPASS_RADIANS):
		self.Class = 'Compass'
		self.units = units
		self.roll = 0
		self.pitch = 0
		self.heading = 0
		self.stamp = time.time()
		if data:
			for key in data:
				setattr(self, key, data[key])

	def set(self, x, y, z):
		self.roll = x
		self.pitch = y
		self.heading = z

	def __str__(self):
		s = 'r: {:.2f} p: {:.2f} h: {:.2f} {}'.format(self.roll, self.pitch, self.heading, self.kind[self.units])
		return s


@froze_it
class IMU(object):
	"""
	Simple tilt compensated compass message, the roll, pitch, and heading angles
	are stored either in radians or degrees.
	"""
	IMU_RADIANS = 0
	IMU_DEGREES = 1
	kind = {
		0: 'Rads',
		1: 'Deg'
	}

	def __init__(self, data=None):
		self.Class = 'IMU'
		self.linear_acceleration = Vector()
		self.angular_velocity = Vector()
		self.orientation = Quaternion()
		self.stamp = time.time()

		if data:
			for key in data:
				if key in ['linear_acceleration', 'angular_velocity']:
					setattr(self, key, Vector(data[key]))
				elif key == 'orientation':
					setattr(self, key, Quaternion(data[key]))
				else:
					setattr(self, key, data[key])

	def __str__(self):
		# s = 'a: ' + self.linear_acceleration.__str__()
		# s += 'g: ' + self.angular_velocity.__str__()
		# s += 'q: ' + self.orientation.__str__()
		s = 'IMU: a: {} w: {} q: {}'.format(self.linear_acceleration, self.angular_velocity, self.orientation)
		return s


@froze_it
class Image(object):
	def __init__(self, data=None):
		self.depth = -1   # 0-grayscale, 1-bgr ... why?
		self._img = None  # image, either numpy or b64
		self.b64 = False  # is this encoded for transmission?
		self.stamp = time.time()
		self.Class = 'Image'

		if data:
			for key in data:
				setattr(self, key, data[key])

	def __str__(self):
		if self._img is None:
			s = 'image empty'
		elif not self.b64:
			w, h = self.img.shape[:2]
			depth = 'color' if self.depth else 'gray'
			s = 'Image[{}] w:{} h:{}'.format(depth, w, h)
		else:
			s = 'image is b46 encoded'

		return s

	@property
	def img(self):
		return self._img

	@img.setter
	def img(self, image):
		shp = image.shape
		if len(shp) == 2:
			self.depth = 0  # grayscale
		elif len(shp) == 3:
			self.depth = 1  # color ... why not shp[2]
		else:
			print 'crap, wrong shape {}'.format(shp)
		self._img = image

	@staticmethod
	def randomImage(size=(5, 5)):
		np.random.randint(0, 255, size=size)

	def decodeB64(self):
		if self.b64:
			ii = base64.b64decode(self._img)
			ii = np.fromstring(ii, dtype=np.uint8)
			ii = cv2.imdecode(ii, self.depth)
			self._img = ii
			self.b64 = False

	def encodeB64(self):
		if not self.b64:
			jpeg = cv2.imencode('.jpg', self._img)[1]
			b64 = base64.b64encode(jpeg)
			self._img = b64
			self.b64 = True


@froze_it
class Twist(object):
	def __init__(self, data=None):
		self.Class = 'Twist'
		self.linear = Vector()
		self.angular = Vector()
		self.stamp = time.time()

		if data:
			for key in data:
				if key in ['linear', 'angular']:
					setattr(self, key, Vector(data[key]))
				else:
					setattr(self, key, data[key])

	def __str__(self):
		s = 'linear: {:2f} {:2f} {:2f} '.format(self.linear.x, self.linear.y, self.linear.z)
		s += 'angular: {:2f} {:2f} {:2f}'.format(self.angular.x, self.angular.y, self.angular.z)
		# s += '\n' + str(self.img)
		return s


@froze_it
class Wrench(object):
	def __init__(self, data=None):
		self.Class = 'Wrench'
		self.force = Vector()
		self.torque = Vector()
		self.stamp = time.time()

		if data:
			for key in data:
				if key in ['torque', 'force']:
					setattr(self, key, Vector(data[key]))
				else:
					setattr(self, key, data[key])

	def __str__(self):
		return 'Wrench: force: {} torque: {}'.format(self.force, self.torque)


@froze_it
class Pose(object):
	def __init__(self, data=None):
		self.Class = 'Pose'
		self.position = Vector()
		self.orientation = Quaternion()
		self.stamp = time.time()

		if data:
			for key in data:
				if key == 'position':
					setattr(self, key, Vector(data[key]))
				elif key == 'orientation':
					setattr(self, key, Quaternion(data[key]))
				else:
					setattr(self, key, data[key])

	def __str__(self):
		s = 'Pose: position: {}, orientation: {}'.format(self.postion, self.orientataion)
		return s


@froze_it
class Range(object):
	UNKNOWN = 0
	ULTRASOUND = 1
	LIDAR = 2
	IR = 3
	kind = {
		0: 'Unknown',
		1: 'Ultrasound',
		2: 'Lidar',
		3: 'IR'
	}

	def __init__(self, data=None):
		self.Class = 'Range'
		self.range = []
		self.fov = 0.0
		self.type = self.UNKNOWN
		self.stamp = time.time()

		if data:
			for key in data:
				setattr(self, key, data[key])

	def __str__(self):
		s = 'Range[{}]: {}'.format(self.kind[self.type], self.range)
		return s


@froze_it
class Power(object):
	def __init__(self, data=None):
		self.Class = 'Power'
		self.current = 0.0
		self.voltage = 0.0
		self.stamp = time.time()

		if data:
			for key in data:
				setattr(self, key, data[key])

	def __str__(self):
		return 'Power: current: {} voltage: {}'.format(self.current, self.voltage)


@froze_it
class Odom(object):
	def __init__(self, data=None):
		self.Class = 'Odom'
		self.position = Pose()
		self.velocity = Twist()
		self.stamp = time.time()

		if data:
			for key in data:
				if key == 'position':
					setattr(self, key, Pose(data[key]))
				elif key == 'orientation':
					setattr(self, key, Twist(data[key]))
				else:
					setattr(self, key, data[key])

	def __str__(self):
		return 'Odom: position: {} velocity: {}'.format(self.position, self.velocity)


class Axes(object):
	def __init__(self, data=None):
		self.Class = 'Axes'
		self.leftStick = [0.0, 0.0]
		self.rightStick = [0.0, 0.0]
		self.dPad = [0.0, 0.0]
		self.L2 = 0.0
		self.R2 = 0.0

		if data:
			for key in data:
				setattr(self, key, data[key])

	def set(self, ls, rs, dp, l2, r2):
		self.leftStick = ls
		self.rightStick = rs
		self.dPad = dp
		self.L2 = l2
		self.R2 = r2


class Buttons(object):
	def __init__(self, data=None):
		self.Class = 'Buttons'
		self.x = False
		self.o = False
		self.s = False
		self.t = False
		self.R1 = False
		self.L1 = False
		self.L3 = False
		self.R3 = False
		self.options = False
		self.share = False

		if data:
			for key in data:
				setattr(self, key, data[key])

	def set(self, x, o, s, t, r1, l1, r3, l3, opt, share):
		self.x = x
		self.o = o
		self.s = s
		self.t = t
		self.R1 = r1
		self.L1 = l1
		self.L3 = l3
		self.R3 = r3
		self.options = opt
		self.share = share


@froze_it
class Joystick(object):
	"""
	This is a joystick message and setup to only support a PS4 controller ...
	suck it XBox! :)
	"""
	def __init__(self, data=None):
		self.Class = 'Joystick'
		self.axes = Axes()
		self.buttons = Buttons()
		self.stamp = time.time()

		if data:
			for key in data:
				if key == 'axes':
					setattr(self, key, Axes(data[key]))
				elif key == 'buttons':
					setattr(self, key, Buttons(data[key]))
				else:
					setattr(self, key, data[key])

	def __str__(self):
		return 'Joystick not setup'


@froze_it
class Array(object):
	"""
	Array
	"""
	def __init__(self, data=None):
		self.Class = 'Array'
		self.array = []
		# self.stamp = time.time()

		if data:
			for key in data:
				print('Array >>', key, data[key])
				# setattr(self, key, list(data[key]))
				setattr(self, key, data[key])

	def __str__(self):
		return 'Array[{}]: {}'.format(len(self.array), self.array)


def serialize(c):
	"""
	Takes a message and turns it into a json string.
	"""
	if c.Class == 'Image':
		c.encodeB64()
	return json.dumps(c, default=lambda o: vars(o))


idc = {
	'Image': Image,
	'Vector': Vector,
	'Quaternion': Quaternion,
	'Wrench': Wrench,
	'Pose': Pose,
	'Twist': Twist,
	'IMU': IMU,
	'Odom': Odom,
	'Axes': Axes,
	'Buttons': Buttons,
	'Joystick': Joystick,
	'Compass': Compass,
	'Range': Range,
	'Power': Power,
	'Array': Array
}


def deserialize(s):
	"""
	Takes a json string and turns it into a message. If the message is an
	Image, then it automatically decodes it from base64/jpeg
	"""
	j = json.loads(s)
	c = None
	if 'Class' in j and j['Class'] in idc:
		c = idc[j['Class']](j)

		if c.Class == 'Image':
			c.decodeB64()

	return c


def dict_to_class(dct):
	msg = json.dumps(dct)
	clss = deserialize(msg)
	return clss
