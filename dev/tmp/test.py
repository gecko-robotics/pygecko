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

    def rec(self,x):
        if isinstance(x,tuple):
            # print(">> tuple")
            return list(self.rec(i) for i in x)
        # print("*** not tuple ***")
        return x

    def ext_pack2(self, x):
        try:
            # print("pack id", x.id)
            xx = self.rec(x)
            # print(">>", xx)
            xx = msgpack.ExtType(x.id, msgpack.packb(xx, use_bin_type=True, strict_types=True))
            return xx
        except Exception as e:
            print(e)
            # print("wtf:", x[:])
            # print("wtf:", x)
            return x

    def ext_unpack2(self, code, data):
        if code in self.msgs.keys():
            # d = msgpack.unpackb(data, ext_hook=self.ext_unpack2, use_list=False,raw=False)
            # d = msgpack.unpackb(data, ext_hook=self.ext_unpack2, use_list=False,raw=False)
            d = msgpack.unpackb(data, use_list=False,raw=False)
            # print("code:",code,"unpack data:", d)
            return self.msgs[code](*d)
        return msgpack.ExtType(code, data)

    def pack(self, data):
        return msgpack.packb(data, use_bin_type=True, strict_types=True,default=self.ext_pack2)

    def unpack(self, data):
        return msgpack.unpackb(data, use_list=False,raw=False, ext_hook=self.ext_unpack2)


mp = MsgPacker()


def printMsg(m):
    # print("msg:", m[:], " len:", len(m))
    mc = mp.pack(m)
    rm = mp.unpack(mc)
    # print(m)
    # print(rm)
    print(">> {}[{}] packed {} ... {}".format(
            m.__class__.__name__,
            m.id,
            len(mc),
            m == rm
        )
    )
    if 'timestamp' in m._fields:
        assert m.timestamp == rm.timestamp
    assert m == rm
    # print(">>", mp.unpack(mc))


v = vec_t(1000.123456789,-2.3456789,0.00003)
# print(v[:])
printMsg(v)
printMsg(quaternion_t(1,2,3,4))
printMsg(wrench_t(v,v))
printMsg(pose_t(v,v))
printMsg(twist_t(v,v))
printMsg(joystick_t(v,(1,2,3,4,5),0))
printMsg(imu_st(v,v,vec_t(-1,2000,1e-3)))
