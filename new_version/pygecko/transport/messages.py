##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################
from collections import namedtuple
import time
import msgpack


class Messages(object):
    msgs = ['Quaternion', 'Vector', 'Pose', 'Image', 'Lidar', 'IMU']
    def __init__(self, new_msgs=None):
        if new_msgs:
            for m in new_msgs:
                self.msgs.append(m)

    def serialize(self, x):
        if x.__class__.__name__ in self.msgs:
            return msgpack.ExtType(1, msgpack.packb([x.__class__.__name__,] + list(x[:]), default=self.serialize, strict_types=True))
        return x

    def deserialize(self, code, data):
        if code == 1:
            # you call this again to unpack and ext_hook for nested
            d = msgpack.unpackb(data, ext_hook=self.deserialize, raw=False)

            # print d[0]   # holds class name
            # print d[1:]  # holds data inorder
            # finds constructor in namespace and calls it
            return globals()[d[0]](*d[1:])
        return msgpack.ExtType(code, data)


# if i use this: use_list=False
# then do i change the below to a tuple?
# def ext_pack(x):
def serialize(x):
    if x.__class__.__name__ in ['Quaternion', 'Vector', 'Pose', 'Image', 'Lidar', 'IMU']:
        return msgpack.ExtType(1, msgpack.packb([x.__class__.__name__,] + list(x[:]), default=serialize, strict_types=True))
    return x


# def ext_unpack(code, data):
def deserialize(code, data):
    if code == 1:
        # you call this again to unpack and ext_hook for nested
        d = msgpack.unpackb(data, ext_hook=deserialize, raw=False)

        # print d[0]   # holds class name
        # print d[1:]  # holds data inorder
        # finds constructor in namespace and calls it
        return globals()[d[0]](*d[1:])
    return msgpack.ExtType(code, data)


def makets():
    """
    returns a timestamp
    """
    return time.time()


def formatts(ts):
    return "fixme"


# simple ones, no stamp, wouldn't just send these. They are datatypes that
# get put into a messagel
#
# cant do: func(*Vector); you would pass in timestamp too!
# but you could do: func(Vector[:3]); cut off stamp
Vector2 = namedtuple('Vector2', 'x y')
Vector = namedtuple('Vector', 'x y z')
Quaternion = namedtuple('Quaternion', 'w x y z')

"""
OpenCV images
-------------------------------
d = img.tobytes()
s = img.shape
msg = Image(s, d, makets())

img = np.frombytes(msg.d, dtype=np.uint8)
img.reshape(msg.shape)
"""

# with timestamp
# CompressedImage = namedtuple('CompressedImage', 'shape data timestamp')
# Image = namedtuple('Image', 'shape data timestamp')
# Lidar = namedtuple('Lidar', 'len data timestamp')
# Path = namedtuple("Path", 'path')


class Image(namedtuple('Image', 'shape bytes timestamp')):
    """
    OpenCV images
    -------------------------------
    d = img.tobytes()
    s = img.shape
    msg = Image(s, d)

    img = np.frombytes(msg.d, dtype=np.uint8)
    img.reshape(msg.shape)
    """
    __slots__ = ()

    def __new__(cls, s, b, ts=None):
        if ts:
            return cls.__bases__[0].__new__(cls, s, b, ts)
        else:
            return cls.__bases__[0].__new__(cls, s, b, time.time())


class Pose(namedtuple('Pose', 'position orientation timestamp')):
    """
    """
    __slots__ = ()

    def __new__(cls, p, o, ts=None):
        if ts:
            return cls.__bases__[0].__new__(cls, p, o, ts)
        else:
            return cls.__bases__[0].__new__(cls, p, o, time.time())


class IMU(namedtuple('IMU', 'linear_accel angular_vel magnetic_field timestamp')):
    """
    """
    __slots__ = ()

    def __new__(cls, a, g, m, ts=None):
        if ts:
            return cls.__bases__[0].__new__(cls, a, g, m, ts)
        else:
            return cls.__bases__[0].__new__(cls, a, g, m, time.time())
