##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################
from __future__ import print_function, division
import time
import msgpack


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


class BagWriteError(Exception):
    pass


class BagWriter(object):
    """
    """

    def __init__(self, filename='data.bag', buffer_size=500, pack=None):
        """
        filename: either a string containing the desired file name (note that
          .bag is appended) OR a file-like object from io.Bytes or something
        buffer_size: number of Bytes, default 10MB
        """
        self.pack = pack
        self.buffer = []
        self.ext_pack = pack
        self.fd = None
        self.buffer_size = buffer_size

        # check to see if this is a file-like object
        # if (hasattr(filename, 'read') and hasattr(filename, 'write')):
        #     self.fd = filename
        #     self.filename = None
        # # append .bag to end of filename if necessary
        # else:
        if filename.rfind('.bag') < 0:
            filename = filename + '.bag'
        self.filename = filename

        if pack:
            # print('pack', pack)

            # must have strict_types for namedtuple to work!!!!!!
            self.packer = msgpack.Packer(default=pack, use_bin_type=True, strict_types=True)
            # self.packer = msgpack.Packer(default=pack, use_bin_type=True)
        else:
            # self.packer = msgpack.Packer(use_bin_type=True)
            self.packer = msgpack.Packer(use_bin_type=True, strict_types=True)

        # print(self.packer)
        # print(dir(self.packer))

    def __del__(self):
        self.close()  # this kills me on BytesIO, it closes the buffer

    def open(self):
        """
        Open data file
        """
        self.fd = open(self.filename, "wb")

    def close(self):
        """
        Flushes any remaining data and closes data file. self.fd = None now.
        """
        if len(self.buffer) > 0:
            self.write()
        if self.fd:
            self.fd.close()
            self.fd = None
            # print('closed', self.filename)

    def push(self, key, msg):
        """
        Push another message and a key into the buffer. Once the buffer limit
        is reached it is written to a file.
        """
        # this has to be a list!!!
        self.buffer.append([key, msg])

        if len(self.buffer) >= self.buffer_size:
            # print('- bag wrote:', len(self.buffer))
            self.write()

    def push_stamp(self, key, msg):
        """
        Push another message and a key into the buffer. Once the buffer limit
        is reached it is written to a file.
        """
        # this has to be a list!!!
        self.buffer.append([key, [msg, time.time()]])

        if len(self.buffer) >= self.buffer_size:
            # print('- bag wrote:', len(self.buffer))
            self.write()

    def write(self):
        # check if buffer is empty
        if len(self.buffer) == 0:
            return

        # if file is not open then open the file for writing
        if self.fd is None:
            self.open()

        for d in self.buffer:
            self.fd.write(self.packer.pack(d))

        # reset buffer to empty
        self.buffer = []

    @staticmethod
    def read(filename):
        """
        Given a filename, it opens it and read all data into memory and return
        Inputs:
          filename - name of file
        Return:
          dict() with keys for each recorded data stream and a list/tuple of
          data points
        """
        data = {}
        # check to see if this is a file-like object
        # if (hasattr(filename, 'read') and hasattr(filename, 'write')):
        #     fd = filename
        # else:
        fd = open(filename, 'rb')

        if self.ext_unpack:
            # print('unpacker')
            unpacker = msgpack.Unpacker(fd, ext_hook=self.ext_unpack, raw=False)
        else:
            unpacker = msgpack.Unpacker(fd, raw=False)

        for o in unpacker:
            key = o[0]
            value = o[1]
            if key not in data:
                data[key] = []
            data[key].append(value)

        return data



# or

class MsgBox(object):
    def __init__(self, fname, buffer_size=500):
        self.fd = open(fname, 'w')
        self.buffer = {}
        self.buffer_size = buffer_size
        self.counter = 0

    def __del__(self):
        if self.counter > 0:
            self.write()
        self.close()

    def push(self, topic, data):
        # self.buffer.append(data)
        # if topic not in self.buffer:
        try:
            self.buffer[topic].append(data)
        except KeyError:
            self.buffer[topic] = []
            self.buffer[topic].append(data)

        # self.buffer[topic].append(data)
        self.counter += 1
        if self.counter > self.buffer_size:
            self.write()

    def write(self):
        print('>> write', self.buffer)
        json.dump(self.buffer, self.fd)
        self.buffer = {}
        self.counter = 0
        if self.fd.closed:
            print("file closed")

    def close(self):
        if self.counter > 0:
            self.write()
        if not self.fd.closed:
            self.fd.close()

    @staticmethod
    def read(fname):
        data = {}
        try:
            fd = open(fname, "r")
            while True:
                d = json.load(fd)
                for k, v in d.items():
                    try:
                        data[k] += v
                    except KeyError:
                        data[k] = []
                        data[k] += v
                print('>> read', d)
        except EOFError:
            pass
        return data
