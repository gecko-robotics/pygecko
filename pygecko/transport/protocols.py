# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2014 Kevin Walchko
# see LICENSE for full details
##############################################
#

import pickle

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
        def pack(self, data):
            return msgpack.packb(data, use_bin_type=True, strict_types=True)

        def unpack(self, data):
            return msgpack.unpackb(data, raw=False)


    class MsgPackCustom(object):
        def __init__(self, packer, unpacker):
            self.packer = packer
            self.ext_unpack = unpacker

        def pack(self, data):
            return msgpack.packb(data, use_bin_type=True, strict_types=True,default=self.packer)

        def unpack(self, data):
            return msgpack.unpackb(data, raw=False, ext_hook=self.ext_unpack)

except ImportError:
    class MsgPack():
        pass
    class MsgPackCustom():
        pass
