##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################
from collections import namedtuple
from enum import Enum, IntFlag
import time

GeckoMsgFlags = IntFlag(
    'GeckoMsgFlags',
    {
        'vector':    0,
        'quaternion': 1,
        'twist':     4,
        'wrench':    2,
        'pose':      3,
        'imu':       10,
        'joystick':  11,
        'lidar':     20
    }
)

GeckoMsgs = list(GeckoMsgFlags)

# simple ones, no stamp, wouldn't just send these. They are datatypes that
# get put into a messages
# Vector2 = namedtuple('Vector2', 'x y')
# Vector = namedtuple('Vector', 'x y z')
# Quaternion = namedtuple('Quaternion', 'w x y z')
# Twist = namedtuple('Twist', 'linear angular')
# Wrench = namedtuple('Wrench', 'force torque')
# Pose = namedtuple('Pose', 'position orientation')  # value?
# Joystick = namedtuple('Joystick', 'axes buttons type')
Log = namedtuple('Log', 'level name text')

# with timestamp
# CompressedImage = namedtuple('CompressedImage', 'shape data timestamp')
# Image = namedtuple('Image', 'shape data timestamp')
# Lidar = namedtuple('Lidar', 'len data timestamp')
# Path = namedtuple("Path", 'path')

# class vec_t(namedtuple('vec_t', 'x y z')):
#     __slots__ = ()
#
#     def __new__(cls, p, o, ts=None):
#         return cls.__bases__[0].__new__(cls, x,y,z)

# class Image(namedtuple('Image', 'shape bytes compressed timestamp')):
#     """
#     OpenCV images
#     -------------------------------
#     d = img.tobytes()
#     s = img.shape
#     msg = Image(s, d)
#
#     img = np.frombuffer(msg.d, dtype=np.uint8)
#     img.reshape(msg.shape)
#     -------------------------------
#     You can compress the image by passing compress=True ... the compression
#     ratio is not very high
#     """
#     __slots__ = ()
#
#     def __new__(cls, s, b, c=False, ts=None):
#         if ts:
#             return cls.__bases__[0].__new__(cls, s, b, c, ts)
#         else:
#             return cls.__bases__[0].__new__(cls, s, b, c, time.time())
#
# class PoseStamped(namedtuple('Pose', 'position orientation timestamp')):
#     """
#     Pose refers to the positiona and orientation of a robot.
#     """
#     __slots__ = ()
#
#     def __new__(cls, p, o, ts=None):
#         if ts:
#             return cls.__bases__[0].__new__(cls, p, o, ts)
#         else:
#             return cls.__bases__[0].__new__(cls, p, o, time.time())
#
#
# class IMU(namedtuple('IMU', 'linear_accel angular_vel magnetic_field timestamp')):
#     """
#     Inertial measurement unit
#     """
#     __slots__ = ()
#
#     def __new__(cls, a, g, m, ts=None):
#         if ts:
#             return cls.__bases__[0].__new__(cls, a, g, m, ts)
#         else:
#             return cls.__bases__[0].__new__(cls, a, g, m, time.time())
#
# class Lidar(namedtuple('Lidar', 'scan timestamp')):
#     """
#     Inertial measurement unit
#     """
#     __slots__ = ()
#
#     def __new__(cls, s, ts=None):
#         if ts:
#             return cls.__bases__[0].__new__(cls, s, ts)
#         else:
#             return cls.__bases__[0].__new__(cls, s, time.time())


###########################################################################
###########################################################################

class vec_t(namedtuple('vec_t', 'x y z')):
    __slots__ = ()

    def __new__(cls, x,y,z):
        cls.id = 0
        return cls.__bases__[0].__new__(cls,x,y,z)

class quaternion_t(namedtuple('quaternion_t', 'w x y z')):
    __slots__ = ()

    def __new__(cls, w,x,y,z):
        cls.id = 1
        return cls.__bases__[0].__new__(cls,w,x,y,z)


class wrench_t(namedtuple('wrench_t', 'force torque')):
    __slots__ = ()

    def __new__(cls, f,t):
        cls.id = 2
        return cls.__bases__[0].__new__(cls,f,t)

class pose_t(namedtuple('pose_t', 'position orientation')):
    __slots__ = ()

    def __new__(cls, p,o):
        cls.id = 3
        return cls.__bases__[0].__new__(cls,p,o)

class twist_t(namedtuple('twist_t', 'linear angular')):
    __slots__ = ()

    def __new__(cls, l,a):
        cls.id = 4
        return cls.__bases__[0].__new__(cls,l,a)

class imu_st(namedtuple('imu_st', 'linear_accel angular_vel magnetic_field timestamp')):
    """
    Inertial measurement unit
    """
    __slots__ = ()

    def __new__(cls, a, g, m, ts=None):
        cls.id = 10
        if ts:
            return cls.__bases__[0].__new__(cls, a, g, m, ts)
        else:
            return cls.__bases__[0].__new__(cls, a, g, m, time.time())


class joystick_st(namedtuple('joystick_t', 'axes buttons type timestamp')):
    __slots__ = ()

    def __new__(cls, a,b,t, ts=None):
        cls.id = 11
        if ts:
            return cls.__bases__[0].__new__(cls,a,b,t,ts)
        else:
            return cls.__bases__[0].__new__(cls,a,b,t,time.time())

class lidar_st(namedtuple('lidar_st', 'data timestamp')):
    """
    Inertial measurement unit
    """
    __slots__ = ()

    def __new__(cls, s, ts=None):
        cls.id = 20
        if ts:
            return cls.__bases__[0].__new__(cls, s, ts)
        else:
            return cls.__bases__[0].__new__(cls, s, time.time())
