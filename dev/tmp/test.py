#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import namedtuple
import time
import msgpack
import zlib

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

class joystick_t(namedtuple('joystick_t', 'axes buttons type')):
    __slots__ = ()

    def __new__(cls, a,b,t):
        cls.id = 4
        return cls.__bases__[0].__new__(cls,a,b,t)


class twist_t(namedtuple('twist_t', 'linear angular')):
    __slots__ = ()

    def __new__(cls, l,a):
        cls.id = 5
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

###########################################

class MsgPacker(object):
    msgs = {
        0: vec_t,
        1: quaternion_t,
        2: wrench_t,
        3: pose_t,
        4: joystick_t,
        5: twist_t,
        10: imu_st
    }

    def ext_pack2(self, x):
        try:
            return msgpack.ExtType(x.id, msgpack.packb(list(x[:]), default=self.ext_pack2, strict_types=True))
        except:
            return x

    def ext_unpack2(self, code, data):
        # print(">>", code)
        if code in self.msgs.keys():
            d = msgpack.unpackb(data, ext_hook=self.ext_unpack2, raw=False)
            return self.msgs[code](*d)
        return msgpack.ExtType(code, data)

    def pack(self, data):
        return msgpack.packb(data, use_bin_type=True, strict_types=True,default=self.ext_pack2)

    def unpack(self, data):
        return msgpack.unpackb(data, raw=False, ext_hook=self.ext_unpack2)

mp = MsgPacker()

v = vec_t(1,2,3)
print(v)
print(v.id)

mv = mp.pack(v)
print(mv)
print("packed",len(mv))

i = imu_st(v,v,vec_t(-1,2000,1e-3))
print(i)
mi = mp.pack(i)
print("packed",len(mi))

print(mi)

ii = mp.unpack(mi)
print(ii)
