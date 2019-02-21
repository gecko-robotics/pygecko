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

class imu_st(namedtuple('imu_st', 'linear_accel angular_vel magnetic_field timestamp')):
    """
    Inertial measurement unit
    """
    __slots__ = ()

    def __new__(cls, a, g, m, ts=None):
        cls.id = 2
        if ts:
            return cls.__bases__[0].__new__(cls, a, g, m, ts)
        else:
            return cls.__bases__[0].__new__(cls, a, g, m, time.time())

# def ext_pack(x):
#     try:
#         return msgpack.ExtType(1, msgpack.packb([x.id,] + list(x[:]), default=ext_pack, strict_types=True))
#     except:
#         return x
#
# def ext_unpack(code, data):
#     msgs = {
#         0: 'vec_t',
#         2: 'imu_st'
#     }
#     if code == 1:
#         # you call this again to unpack and ext_hook for nested
#         d = msgpack.unpackb(data, ext_hook=ext_unpack, raw=False)
#
#         # print d[0]   # holds class name
#         # print d[1:]  # holds data inorder
#         # finds constructor in namespace and calls it
#         return globals()[msgs[d[0]]](*d[1:])
#     return msgpack.ExtType(code, data)


###########################################

def ext_pack2(x):
    try:
        return msgpack.ExtType(x.id, msgpack.packb(list(x[:]), default=ext_pack2, strict_types=True))
    except:
        return x

msgs = {
    0: vec_t
}
msgs[2] = imu_st  # add new msg class

def ext_unpack2(code, data):
    # print(">>", code)
    if code in msgs.keys():
        d = msgpack.unpackb(data, ext_hook=ext_unpack2, raw=False)
        return msgs[code](*d)
    return msgpack.ExtType(code, data)


v = vec_t(1,2,3)
print(v)
print(v.id)

mv=msgpack.packb(v, use_bin_type=True, strict_types=True,default=ext_pack2)
print(mv)
print("packed",len(mv))

i = imu_st(v,v,vec_t(-1,2000,1e-3))
print(i)
mi=msgpack.packb(i, use_bin_type=True, strict_types=True,default=ext_pack2)
print("packed",len(mi))

print(mi)

ii=msgpack.unpackb(mi, raw=False, ext_hook=ext_unpack2)
print(ii)
