#!/usr/bin/env python

import time
import simplejson as json  # supposed to be better than json
import math
import numpy as np


def serialize(c):
	"""
	Takes a dictionary and turns it into a json string.
	"""
	return json.dumps(c, default=lambda o: vars(o))


def deserialize(s):
	"""
	Takes a json string and turns it into a dictionary.
	"""
	return json.loads(s)


class Message(dict):
	"""
	Base class for all messages. Main jobs:
	- prevent new keys being added, don't want a 3d vector with keys
		of [x,y,z,tom,hi,sam]
	"""
	def __init__(self):
		dict.__init__(self)

	def __setitem__(self, key, newvalue):
		"""
		Doesn't allow new keys to be added to dict.
		"""
		if key in self:
			dict.__setitem__(self, key, newvalue)
		else:
			raise KeyError('key {} not part of message format'.format(key))

	def update(self, E):
		"""
		Doesn't allow new keys to be added to dict.
		"""
		for key, value in E.items():
			self.__setitem__(key, value)


class Vector(Message):
	"""
	Handles vectors

	Shortcut to set:
	v = Vector(x=1, y=33, z=55)
	v.update(y=44, z=22)
	"""
	def __init__(self, **kw):
		Message.__init__(self)
		default = {'x': 0.0, 'y': 0.0, 'z': 0.0}
		dict.update(self, default)
		if kw: dict.update(self, kw)

	def __str__(self):  # pretty up the print statement
		return 'Vector[x,y,z]: {:.4f} {:.4f} {:.4f}'.format(self.get('x'), self.get('y'), self.get('z'))

	def norm(self):
		m = self.values()
		return math.sqrt(m[0]**2 + m[1]**2 + m[2]**2)


class Quaternion(Message):
	def __init__(self, **kw):
		Message.__init__(self)
		default = {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 1.0}
		dict.update(self, default)
		if kw:
			dict.update(self, kw)
			m = self.values()
			d = math.sqrt(m[0]**2 + m[1]**2 + m[2]**2 + m[3]**2)
			# print d
			if d > 0.0:
				for k, v in self.items():
					# print k,v
					dict.update(self, {k: v / d})

	def __str__(self):  # pretty up the print statement
		return 'Quaternion[x,y,z,w]: {:.4f} {:.4f} {:.4f} {:.4f}'.format(self.get('x'), self.get('y'), self.get('z'), self.get('w'))
# q=Quaternion(x=1,y=3,w=4); print q


class Twist(Message):
	"""
	Twist is a combined linear and angular motion

	t = Twist()
	t['linear'].update(x=22, z=33)
	"""
	def __init__(self):
		Message.__init__(self)
		dict.update(self, linear=Vector())
		dict.update(self, angular=Vector())

	def __str__(self):  # pretty up the print statement
		return 'Twist:\n\tLinear {}\n\tAngular {}'.format(self.get('linear'), self.get('angular'))


class Wrench(Message):
	def __init__(self):
		Message.__init__(self)
		dict.update(self, force=Vector())
		dict.update(self, torque=Vector())


class Pose(Message):
	def __init__(self):
		Message.__init__(self)
		dict.update(self, position=Vector())
		dict.update(self, orientation=Quaternion())


class PoseStamped(Message):
	"""
	This is primarily used in path planning. The planner returns a position/orientation
	at a given time.
	"""
	def __init__(self):
		Message.__init__(self)
		dict.update(self, stamp=time.time())
		dict.update(self, position=Vector())
		dict.update(self, orientation=Quaternion())


class Range(Message):
	"""
	Holds the ranges of the Sharp IR sensors. Note, currently, these are just digital and
	only return True (1) or False (0) and have a real distance of around 7 inches. This
	is because the analog signal is tied to a digital pin.
	"""
	def __init__(self):
		Message.__init__(self)
		dict.update(self, stamp=time.time())
		dict.update(self, fov=20.0)  # need to fix this
		dict.update(self, limits=(0.01, 0.08))
		dict.update(self, range=[0, 0, 0, 0, 0, 0, 0, 0])  # this is for all 8 IR's


class IMU(Message):
	"""
	"""
	def __init__(self):
		Message.__init__(self)
		dict.update(self, stamp=time.time())
		dict.update(self, linear_acceleration=Vector())
		dict.update(self, angular_velocity=Vector())
		dict.update(self, orientation=Quaternion())
		dict.update(self, heading=0.0)  # degrees
		dict.update(self, temperature=0.0)  # degrees C

	def __str__(self):
		return 'IMU:\n\tLinear Accel {}\n\tAngular Vel {}\n\tOrientation {}\n\tHeading [deg]: {}\n\tTemp [C]: {}'.format(
			self.get('linear_acceleration'), self.get('angular_velocity'),
			self.get('orientation'), self.get('heading'), self.get('temperature')
		)


class Odom(Message):
	"""
	"""
	def __init__(self):
		Message.__init__(self)
		dict.update(self, stamp=time.time())
		dict.update(self, position=Pose())
		dict.update(self, velocity=Twist())


class Path(Message):
	"""
	The returned path from a path planner which is an array of position/orientation at various times. These poses take the robot from the start to the stop position of the getPlan message.
	"""
	def __init__(self):
		Message.__init__(self)
		dict.update(self, stamp=time.time())
		dict.update(self, poses=[])


class GetPlan(Message):
	"""
	Define the start and stop position/orientation/time for a path planner
	"""
	def __init__(self):
		Message.__init__(self)
		dict.update(self, start=PoseStamped())
		dict.update(self, stop=PoseStamped())


class Text(Message):
	"""
	Simple text message
	"""
	def __init__(self, **kw):
		Message.__init__(self)
		dict.update(self, stamp=time.time())
		dict.update(self, message='')
		if kw: dict.update(self, kw)


class Compass(Message):
	"""
	Simple tilt compensated compass message, the roll, pitch, and heading angles
	are stored either in radians or degrees.
	"""
	COMPASS_RADIANS = 0
	COMPASS_DEGREES = 1

	def __init__(self, roll=0, pitch=0, heading=0):
		Message.__init__(self)
		dict.update(self, stamp=time.time())
		dict.update(self, roll=roll, pitch=pitch, heading=heading)
		dict.update(self, units=self.COMPASS_RADIANS)


class Image(Message):
	"""
	"""
	IMAGE_FORMAT_UNKNOWN = 0
	IMAGE_FORMAT_JPG     = 1
	IMAGE_FORMAT_PNG     = 2
	IMAGE_FORMAT_NUMPY   = 3

	def __init__(self, img=None, format=None):
		Message.__init__(self)
		dict.update(self, stamp=time.time(), format=0)
		if type(img) == np.ndarray:
			a = img.shape
			if len(a) == 3:
				w, h, d = a
			else:
				w, h = a
				d = 1

			# i would rather do size as a tuple, but json makes it a list
			dict.update(self, image=img, size=[w, h], depth=d)


class BatteryState(Message):
	"""
	"""
	# Power supply status constants
	POWER_SUPPLY_STATUS_UNKNOWN      = 0
	POWER_SUPPLY_STATUS_CHARGING     = 1
	POWER_SUPPLY_STATUS_DISCHARGING  = 2
	POWER_SUPPLY_STATUS_NOT_CHARGING = 3
	POWER_SUPPLY_STATUS_FULL         = 4

	# Power supply health constants
	POWER_SUPPLY_HEALTH_UNKNOWN               = 0
	POWER_SUPPLY_HEALTH_GOOD                  = 1
	POWER_SUPPLY_HEALTH_OVERHEAT              = 2
	POWER_SUPPLY_HEALTH_DEAD                  = 3
	POWER_SUPPLY_HEALTH_OVERVOLTAGE           = 4
	POWER_SUPPLY_HEALTH_UNSPEC_FAILURE        = 5
	POWER_SUPPLY_HEALTH_COLD                  = 6
	POWER_SUPPLY_HEALTH_WATCHDOG_TIMER_EXPIRE = 7
	POWER_SUPPLY_HEALTH_SAFETY_TIMER_EXPIRE   = 8

	# Power supply technology (chemistry) constants
	POWER_SUPPLY_TECHNOLOGY_UNKNOWN = 0
	POWER_SUPPLY_TECHNOLOGY_NIMH    = 1
	POWER_SUPPLY_TECHNOLOGY_LION    = 2
	POWER_SUPPLY_TECHNOLOGY_LIPO    = 3
	POWER_SUPPLY_TECHNOLOGY_LIFE    = 4
	POWER_SUPPLY_TECHNOLOGY_NICD    = 5
	POWER_SUPPLY_TECHNOLOGY_LIMN    = 6

	def __init__(self, img=None):
		Message.__init__(self)
		dict.update(self, stamp=time.time())
		dict.update(self, voltage=0)                  # 7.2 V
		dict.update(self, current=0)                  # 0.45 A
		dict.update(self, design_capacity=0)          # 240 Ahr
		dict.update(self, power_supply_technology=0)  # NiMH
		dict.update(self, power_supply_status=0)      # discharge
		dict.update(self, power_supply_health=0)      # good
		dict.update(self, location='')


class AudioFile(Message):
	"""
	Simple audio message

	kevin@Logan ~ $ file test.wav
	test.wav: RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 16000 Hz
	"""
	AUDIO_FORMAT_WAV = 0  # .wav
	AUDIO_FORMAT_MP3 = 1  # .mp3
	AUDIO_FORMAT_MP4 = 2  # .m4a

	def __init__(self):
		Message.__init__(self)
		dict.update(self, stamp=time.time())
		dict.update(self, file='')


class Joystick(Message):
	def __init__(self):
		# Message.__init__(self)
		Message.__init__(self)
		dict.update(self, stamp=time.time())
		dict.update(self, axes={'leftStick': [0.0, 0.0], 'rightStick': [0.0, 0.0], 'L2': 0.0, 'R2': 0.0, 'dPad': [0.0, 0.0]})
		dict.update(self, buttons={'x': False, 'o': False, 's': False, 't': False, 'R1': False, 'L1': False, 'L3': False, 'R3': False, 'share': False, 'options': False})

	# def __setitem__(self, key, newvalue):
	# 	if key in self:
	# 		dict.__setitem__(self, key, newvalue)
	# 	else:
	# 		raise KeyError('{} not permitted in message'.format(key))

	@staticmethod
	def str(js):
		return js.__str__()

	# def __str__(self):
		s = '--------------------------------------------------\n'
		ps4 = js['buttons']
		s += 'Triangle {} Square {} X {} O {}\n'.format(
			ps4['t'],
			ps4['s'],
			ps4['x'],
			ps4['o']
		)

		s += 'Share {}    Options {}\n'.format(ps4['share'], ps4['options'])

		ps4 = js['axes']
		s += 'Left Analog {:.3f}, {:.3f}	 Right Analog {:.3f}, {:.3f}\n'.format(
			ps4['leftStick'][0],
			ps4['leftStick'][1],
			ps4['rightStick'][0],
			ps4['rightStick'][1],
		)

		ps4 = js['buttons']
		s += 'L1 {}                         R1 {}\n'.format(ps4['L1'], ps4['R1'])
		ps4 = js['axes']
		s += 'L2 {:.3f}                         R1 {:.3f}\n'.format(ps4['L2'], ps4['R2'])
		ps4 = js['buttons']
		s += 'L3 {}                         R3 {}\n'.format(ps4['L3'], ps4['R3'])

		return s


if __name__ == '__main__':
	# print 'run "nosetests -v ./Messages.py" to test'
	v = Vector(x=1.23, y=-1.23, z=32.1)
	# v.set()
	print v
	# print dir(v)

	t = Twist()
	print t

	i = IMU()
	print i

	j = Joystick()
	print Joystick.str(j)
	# j.update(tom='hi')
	# print j
	# j['bob'] = 25
	# print j

	# m = type('Vector', (object,), dict(x=1.23, y=-1.23, z=32.1))
	# print m
	# print dir(m)
	vv = Vector()
	vv.update(dict(x=1.23, y=-1.23, z=32.1))
	print vv

	tt = Twist()
	tt.update(dict(linear=Vector(x=1.23, y=-1.23, z=32.1)))
	# tt['linear']['tom'] = 7
	print tt

	tt2 = Twist()
	tt2.update(dict(linear=dict(x=1.23, y=-1.23, z=32.1)))
	tt2['linear']['tom'] = 7
	print 'does not work if uou use dicts'
	print tt2
	print tt2['linear']['x']

	ff = Twist()
	ss = deserialize(serialize(tt))
	ff.update(ss)
	print ss
	print ff
