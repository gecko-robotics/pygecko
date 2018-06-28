#!/usr/bin/env python

from __future__ import print_function, division
import time
import os
import simplejson as json
import msgpack
from messages import Image
from messages import makets
from messages import serialize, deserialize

"""
need a way to handle numpy, it is nice, but not necessary to use this library

setup.py(
    extras_require = {
        'numpy':  ["numpy"]
    }
)
"""
# try:
#     # import cv2  I don't think I need this
#     import numpy as np
# except ImportError:
#     import warnings
#     warnings.warn('dependency not found, please install to enable xyz feature')
#
#     class numpy(object):
#         def frombytes(a, b):
#             raise Exception("You need to install numpy to use this function")

# or

try:
    import numpy as np

    def image_pack(img):
        d = img.tobytes()
        s = img.shape
        msg = Image(s, d, makets())
        return msg

    def image_unpack(msg):
        img = np.frombytes(msg.d, dtype=np.uint8)
        img.reshape(msg.shape)
        return img

except ImportError:
    import warnings
    warnings.warn('WARNING: numpy is not installed, cannot handle images')

    def image_pack(img):
        raise BagError("numpy not installed")

    def image_unpack(msg):
        raise BagError("numpy not installed")




"""
msgpack-numpy does some stuff, take a look at how it does it
https://github.com/lebedov/msgpack-numpy/blob/master/msgpack_numpy.py

def patch():  not sure i understand this
    setattr(msgpack, 'Packer', Packer)

so now to make everything work, you just do:
import msgpack_numpy as m
m.patch()

seems cool, but i don't understand what is happening
"""


"""
OLD WAY ... ignore

encode:
img_str = cv2.imencode('.jpg', img)[1].tostring()

decode:
nparr = np.fromstring(STRING_FROM_DATABASE, np.uint8)
img = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)

unicode errors with above

jpeg = = cv2.imencode('.jpg', img)[1]
img_str = base64.b64encode(jpeg)

now to reverse:

ii = base64.b64decode(img_str)
ii = np.fromstring(ii, dtype=np.uint8)
ii = cv2.imdecode(ii, self.depth)

"""


class BagError(Exception):
    pass


class Base(object):
    """
    Base class. It holds the encode/decodeB64() functions.

    Defaults:
      encode: .jpg
      use_compression: False
    """
    fd = None

    def open(self, filename):
        pass


class BagReader(Base):
    """
    """
    def read(self, filename):
        """
        Read and return one data message
        """
        pass

    def read_all(self, filename):
        """
        Given a filename, it opens it and read all data into memory and return
        """
        try:
            with open(filename, 'r') as f:
                data = msgpack.unpack(f, raw=False)

        except Exception as e:
            print('Error reading file: {}'.format(filename))
            print(e)
            raise

        return data


class BagWriter(Base):
    """
    """

    def __init__(self, buffer_size=10240):
        """
        buffer_size: number of Bytes, default 10MB
        """
        self.buffer = []
        # self.fd = None
        self.buffer_size = buffer_size

    def __del__(self):
        self.close()
        print('Bag exiting')

    def open(self, filename):
        """
        Open data file
        """
        # append .bag to end of filename if necessary
        if filename.rfind('.bag') < 0:
            filename = filename + '.bag'
        self.fd = open(filename, "w")

    def close(self):
        """
        Close data file
        """
        self.write()
        self.fd.close()

    def push(self, msg):
        """
        Push another message to the buffer and grab time stamp for play back.
        Buffer is serialized, easier to track memory consumption because it is
        all turned into bytes.
        """
        # dmsg = {'ts': time.time(), 'msg': msg}
        m = serialize(msg)
        self.buffer.append(m)

        if len(self.buffer) >= self.buffer_size:
            print('- bag wrote:', len(self.buffer))
            self.write()

    def write(self):
        if self.fd is None:
            # how do we get here? it has to be open already ... right?
            raise IOError('Bag: please open file first')

        # check if buffer is empty
        if not self.buffer:
            return

        print('buffer:', self.buffer)

        # for m in self.buffer:
        #     self.fd.write(m)

        self.buffer = []


class Record(object):
    """
    connects to topic(s) and saves to a file
    """
    pass


class Play(object):
    """
    read a bag file and pump the messages into the system
    """
    pass


    #
    # def stringify(self, keys):
    #     """
    #     Images need to be converted to base64 for saving.
    #
    #     keys: key name or array of key names
    #     return: None
    #     """
    #     if type(keys) is list:
    #         # print('list', keys)
    #         for key in keys:
    #             self.data['b64keys'].append(key)
    #     elif type(keys) is str:
    #         # print('str', keys)
    #         self.data['b64keys'].append(keys)
    #     else:
    #         raise Exception('Bag::stringify, invalid input: {}'.format(keys))
    #
    # def push(self, key, data):
    #     """
    #     Saves data with timestamp. If data is in b64keys (it is an image), then
    #     it is base64 encoded before saved. All data is saved as: (data, timestamp)
    #
    #     key: dict key name, if not found, Exception is thrown
    #     data: data to be saved
    #     return: None
    #     """
    #     if key in self.data:
    #         # have to convert images (binary) to strings
    #         if key in self.data['b64keys']:
    #             data = self.encodeB64(data)
    #
    #         timestamp = time.time()
    #         self.data[key].append((data, timestamp))
    #     else:
    #         raise Exception('Bag::push, Invalid key: {}'.format(key))
    #
    # def clear(self):
    #     """
    #     Clears and resets everything.
    #     """
    #     self.data = {}
    #     self.data['b64keys'] = []
    #
    # def open(self, topics):
    #     """
    #     Set topic keys for writing
    #     """
    #     self.clear()
    #     for key in topics:
    #         self.data[key] = []
    #
    # def write(self, filename):
    #     """
    #     Once you write a bag, it is written to disk and the data is cleared
    #     """
    #     if self.data == {}:
    #         return
    #
    #     if self.use_compression:
    #         with gzip.open(filename, 'wb') as f:
    #             # json.dump(self.data, f)
    #             s = json.dumps(self.data).encode('utf8')
    #             f.write(s)
    #     else:
    #         with open(filename, 'wb') as f:
    #             # json.dump(self.data, f)
    #             s = json.dumps(self.data).encode('utf8')
    #             f.write(s)
    #
    #     self.clear()
    #
    # def size(self):
    #     """
    #     Returns dict with the length of data for each key.
    #
    #     size() -> {'key 1': length, 'key 2': length, ...}
    #     """
    #     ret = {}
    #
    #     for key in self.data.keys():
    #         ret[key] = len(self.data[key])
    #
    #     return ret

    # def reset(self):
    #     files = os.listdir('./')
    #     for f in files:
    #         if f == self.filename:
    #             os.remove(self.filename)
    #     self.written = False

    # def size(self):
    #     size = os.path.getsize(self.filename)//(2**10)
    #     # print('{}: {} kb'.format(self.filename, size))
    #     return size
