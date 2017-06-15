#!/usr/bin/env python

from pygecko.Messages import Twist, Image, IMU, Joystick, Vector, Array, Dictionary
from pygecko.Messages import Pose, Compass, Range, Quaternion
from pygecko.Messages import Buttons, Axes
from pygecko.Messages import serialize, deserialize
# from pygecko.lib.ZmqClass import Pub, Sub
import numpy as np
from nose.tools import raises


def test_twist():
	t = Twist()
	t.linear.set(.1, .2, .3)
	t.angular.set(-1, -2., -3)

	m = serialize(t)
	m = deserialize(m)

	assert m.linear == t.linear
	assert m.angular == t.angular
	assert isinstance(t, Twist)
	assert isinstance(m, Twist)
	assert isinstance(t.linear, Vector)
	assert isinstance(t.angular, Vector)
	assert isinstance(m.linear, Vector)
	assert isinstance(m.angular, Vector)
	assert t.stamp == m.stamp
	assert t.Class == m.Class


def test_image():
	im = Image()
	im.img = np.random.randint(0, 255, size=(5, 5))

	msg = serialize(im)
	i = deserialize(msg)

	im.decodeB64()  # serialize destroys original image

	assert isinstance(im, Image)
	assert isinstance(i, Image)
	assert isinstance(im.img, np.ndarray), type(im.img)
	assert isinstance(i.img, np.ndarray), type(i.img)
	assert im.depth == i.depth
	assert i.img.all() == im.img.all()
	assert i.Class == im.Class
	assert i.stamp == im.stamp


def test_vector():
	v = Vector()
	v.x = -0.00001
	v.y = 2.123456789
	v.z = -0.0123456789

	m = serialize(v)
	m = deserialize(m)

	assert v.x == m.x
	assert v.y == m.y
	assert v.z == m.z
	assert type(v) == type(m)
	assert v.Class == m.Class


def test_range():
	v = Range()
	v.range = [1, 2, 3]
	v.range = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
	v.fov = 20.0

	m = serialize(v)
	m = deserialize(m)

	assert v.range == m.range
	assert type(v) == type(m)
	assert v.Class == m.Class
	assert len(v.range) == len(m.range)
	assert v.stamp == m.stamp
	assert v.fov == m.fov


def test_quaternion():
	q = Quaternion()
	q.x = 100
	q.y = -100
	q.z = 0.12345
	q.w = -0.12345
	m = serialize(q)
	m = deserialize(m)

	assert type(q) == type(m) == type(Quaternion())
	assert q.Class == m.Class
	assert q == m


def test_imu():
	p = IMU()
	p.linear_acceleration.set(1, 2, 3)
	p.angular_velocity.set(1, 2, 3)
	p.orientation.set(1, 2, 3, 4)
	m = serialize(p)
	m = deserialize(m)

	assert type(p) == type(m) == type(IMU())
	assert isinstance(m.linear_acceleration, Vector)
	assert isinstance(m.angular_velocity, Vector)
	assert isinstance(m.orientation, Quaternion)
	assert p.linear_acceleration == m.linear_acceleration
	assert p.angular_velocity == m.angular_velocity
	assert p.orientation == m.orientation
	assert p.stamp == m.stamp
	assert p.Class == m.Class


def test_pose():
	p = Pose()
	p.position.set(1, 2, 3)
	p.orientation.set(1, 2, 3, 4)
	m = serialize(p)
	m = deserialize(m)

	assert type(p) == type(m) == type(Pose())
	assert isinstance(m.position, Vector)
	assert isinstance(m.orientation, Quaternion)
	assert p.position == m.position
	assert p.orientation == m.orientation
	assert p.stamp == m.stamp
	assert p.Class == m.Class


def test_compass():
	p = Compass()
	p.set(1, 2, 3)
	m = serialize(p)
	m = deserialize(m)

	assert type(p) == type(m) == type(Compass())
	assert p.roll == m.roll
	assert p.pitch == m.pitch
	assert p.heading == m.heading
	assert p.stamp == m.stamp
	assert p.Class == m.Class


def test_joytstick():
	p = Joystick()
	p.axes.set([1, 1], [2, 2], [3, 3], 4, 5)
	p.buttons.set(True, False, True, False, True, False, True, False, True, False)
	m = serialize(p)
	m = deserialize(m)

	assert type(p) == type(m) == type(Joystick())
	assert isinstance(m.axes, Axes)
	assert isinstance(m.buttons, Buttons)
	assert p.axes.leftStick == m.axes.leftStick
	assert p.axes.rightStick == m.axes.rightStick
	assert p.axes.dPad == m.axes.dPad
	assert p.axes.L2 == m.axes.L2
	assert p.stamp == m.stamp
	assert p.Class == m.Class

	
def test_array():
	a = Array()
	
	for i in range(4):
		a.array.append(i)
	
	m = serialize(a)
	m = deserialize(m)
	assert len(m.array) == 4
	for i in range(4):
		assert m.array[i] == i

		
def test_dictionary():
	d = Dictionary()
	d.dict['bob'] = 5
	m = serialize(p)
	m = deserialize(m)
	assert 'bob' in m.dict
	assert m.dict['bob'] == 5

@raises(Exception)
def test_msg():
	v = Vector()
	v.m = 5.0
