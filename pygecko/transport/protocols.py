# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2014 Kevin Walchko
# see LICENSE for full details
##############################################
#

import pickle
from pygecko.messages import vec_t,quaternion_t,wrench_t,pose_t,joystick_st,twist_t,imu_st, lidar_st
from pygecko.messages import GeckoMsgs, GeckoMsgFlags as gmf

class Pickle(object):
    def pack(self, data):
        return pickle.dumps(data)
    def unpack(self, data):
        return pickle.loads(data)


try:
    import simplejson as json
except ImportError:
    import json

class Json(object):
    def pack(self, data):
        """
        json doesn't know how to handle namedtuples, so store class id for
        unpack
        """
        raise Exception("Json protocol isn't ready yet!!!")
        if type(data) in known_types:
            d = data._asdict()
            d['type'] = unpack_types[type(data)]
        else:
            d = data
        return json.dumps(d)

    def unpack(self, data):
        """
        if data is an ordered dictionary AND it has class id, then create the
        message using the class id
        """
        d = json.loads(data)
        if type(data) is OrderedDict:
            if 'type' in d:
                cls = unpack_types[d['type']]
                d.pop('type', None)
                d = cls(*d.values())
        return d

try:
    import msgpack

    class MsgPack(object):

        def ext_unpack2(self, code, data):
            # print(">> code:", code)
            # print("> data:", data)
            if code in GeckoMsgs:
                d = msgpack.unpackb(data, ext_hook=self.ext_unpack2, use_list=False, raw=False)
                print("> d[{}]: {}".format(code,d))

                if code == gmf.vector:
                    return vec_t(*d)
                elif code == gmf.quaternion:
                    return quaternion_t(*d)
                elif code == gmf.wrench:
                    return wrench_t(vec_t(*d[0]), vec_t(*d[1]))
                elif code == gmf.pose:
                    return pose_t(vec_t(*d[0]), quaternion_t(*d[1]))
                elif code == gmf.twist:
                    return twist_t(vec_t(*d[0]), vec_t(*d[1]))
                elif code == gmf.imu:
                    return imu_st(vec_t(*d[0]), vec_t(*d[1]), vec_t(*d[2]), d[3])
                elif code == gmf.lidar:
                    return lidar_st(d[0], d[1])
                elif code == gmf.joystick:
                    return joystick_st(d[0], d[1], d[2], d[3])
                else:
                    raise Exception("MsgPack::ext_unpack: UNKNOW MSG {}  {}".format(code, d))
            return msgpack.ExtType(code, data)

        def pack(self, data):
            try:
                if data.id in [gmf.vector, gmf.quaternion]:
                    # vector, quaternion
                    m = data[:]
                elif data.id in [gmf.wrench, gmf.pose, gmf.twist, gmf.lidar, gmf.imu, gmf.joystick]:
                    # this should get everything else
                    m = tuple(data)
                else:
                    raise Exception("MsgPack::pack: unknown ExtType {}".format(data))

                m = msgpack.ExtType(data.id, msgpack.packb(m, use_bin_type=True, strict_types=False))
                m = msgpack.packb(m, use_bin_type=True, strict_types=True)
                # print(">> m:", m)
                return m
            except AttributeError:
                return msgpack.packb(data, use_bin_type=True, strict_types=False)

        def unpack(self, data):
            return msgpack.unpackb(data, use_list=False, raw=False, ext_hook=self.ext_unpack2)

    # def ext_pack(x):
    #     name = x.__class__.__name__
    #     if name in ['Vector', 'IMU']:
    #         if name == 'Vector': id = 0
    #         elif name == 'IMU': id = 2
    #         return msgpack.ExtType(1, msgpack.packb([id,] + list(x[:]), default=ext_pack, strict_types=True))
    #     return x
    #
    # def ext_unpack(code, data):
    #     if code == 1:
    #         # you call this again to unpack and ext_hook for nested
    #         d = msgpack.unpackb(data, ext_hook=ext_unpack, raw=False)
    #
    #         # print d[0]   # holds class name
    #         # print d[1:]  # holds data inorder
    #         # finds constructor in namespace and calls it
    #         return globals()[d[0]](*d[1:])
    #     return msgpack.ExtType(code, data)
    #
    # class MsgPack(object):
    #     def pack(self, data):
    #         return msgpack.packb(data, use_bin_type=True, strict_types=True,default=ext_pack)
    #
    #     def unpack(self, data):
    #         return msgpack.unpackb(data, raw=False, ext_hook=self.ext_unpack)
    #
    #
    # class MsgPackCustom(object):
    #     def __init__(self, packer, unpacker):
    #         self.packer = packer
    #         self.ext_unpack = unpacker
    #
    #     def pack(self, data):
    #         return msgpack.packb(data, use_bin_type=True, strict_types=True,default=self.packer)
    #
    #     def unpack(self, data):
    #         return msgpack.unpackb(data, raw=False, ext_hook=self.ext_unpack)

except ImportError:
    class MsgPack():
        pass
    class MsgPackCustom():
        pass
