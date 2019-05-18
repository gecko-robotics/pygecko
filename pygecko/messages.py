##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################
from collections import namedtuple
from enum import IntFlag
# from enum import Enum
import time

GeckoMsgFlags = IntFlag(
    'GeckoMsgFlags',
    {
        'vector':     0,
        'quaternion': 1,
        'wrench':     2,
        'pose':       3,
        'twist':      4,
        'imu':       10,
        'joystick':  11,
        'image':     12,
        'lidar':     20
    }
)

GeckoMsgs = list(GeckoMsgFlags)
Log = namedtuple('Log', 'level name text')

# with timestamp
# CompressedImage = namedtuple('CompressedImage', 'shape data timestamp')
# Image = namedtuple('Image', 'shape data timestamp')
# Lidar = namedtuple('Lidar', 'len data timestamp')
# Path = namedtuple("Path", 'path')


class vec_t(namedtuple('vec_t', 'x y z')):
    __slots__ = ()

    def __new__(cls, x, y, z):
        cls.id = GeckoMsgFlags.vector
        return cls.__bases__[0].__new__(cls, x, y, z)


class quaternion_t(namedtuple('quaternion_t', 'w x y z')):
    __slots__ = ()

    def __new__(cls, w, x, y, z):
        cls.id = GeckoMsgFlags.quaternion
        return cls.__bases__[0].__new__(cls, w, x, y, z)


class wrench_t(namedtuple('wrench_t', 'force torque')):
    __slots__ = ()

    def __new__(cls, f, t):
        cls.id = GeckoMsgFlags.wrench
        return cls.__bases__[0].__new__(cls, f, t)


class pose_t(namedtuple('pose_t', 'position orientation')):
    __slots__ = ()

    def __new__(cls, p, o):
        cls.id = GeckoMsgFlags.pose
        return cls.__bases__[0].__new__(cls, p, o)


class twist_t(namedtuple('twist_t', 'linear angular')):
    __slots__ = ()

    def __new__(cls, l, a):
        cls.id = GeckoMsgFlags.twist
        return cls.__bases__[0].__new__(cls, l, a)


class imu_st(namedtuple('imu_st', 'linear_accel angular_vel magnetic_field timestamp')):
    """
    Inertial measurement unit
    """
    __slots__ = ()

    def __new__(cls, a, g, m, ts=None):
        cls.id = GeckoMsgFlags.imu
        if ts:
            return cls.__bases__[0].__new__(cls, a, g, m, ts)
        else:
            return cls.__bases__[0].__new__(cls, a, g, m, time.time())


class joystick_st(namedtuple('joystick_st', 'axes buttons type timestamp')):
    __slots__ = ()

    def __new__(cls, a, b, t, ts=None):
        cls.id = GeckoMsgFlags.joystick
        if ts:
            return cls.__bases__[0].__new__(cls, a, b, t, ts)
        else:
            return cls.__bases__[0].__new__(cls, a, b, t, time.time())


class image_st(namedtuple('image_st', 'shape bytes compressed timestamp')):
    __slots__ = ()

    def __new__(cls, s, b, c, ts=None):
        cls.id = GeckoMsgFlags.image
        if ts:
            return cls.__bases__[0].__new__(cls, s, b, c, ts)
        else:
            return cls.__bases__[0].__new__(cls, s, b, c, time.time())


# class image2_st(namedtuple('image_st', 'shape bytes timestamp')):
#     __slots__ = ()
#
#     def __new__(cls, img, ts=None, compressed=False):
#         cls.id = GeckoMsgFlags.image
#
#         if compressed:
#             jpg = cv2.imencode('.jpg', img)[1]
#             # m = handler.dumps(img.tobytes())
#             msg = image_st(img.shape, jpg, True)
#         else:
#             msg = image_st(img.shape, img.tobytes(), False)
#         return msg
#
#         if ts:
#             return cls.__bases__[0].__new__(cls, s, b, c, ts)
#         else:
            return cls.__bases__[0].__new__(cls, s, b, c, time.time())


class lidar_st(namedtuple('lidar_st', 'data timestamp')):
    """
    Inertial measurement unit
    """
    __slots__ = ()

    def __new__(cls, s, ts=None):
        cls.id = GeckoMsgFlags.lidar
        if ts:
            return cls.__bases__[0].__new__(cls, s, ts)
        else:
            return cls.__bases__[0].__new__(cls, s, time.time())
