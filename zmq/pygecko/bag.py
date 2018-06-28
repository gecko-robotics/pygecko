#!/usr/bin/env python

from __future__ import print_function, division
import cv2
import time
import numpy as np
import os
import simplejson as json
import base64
import gzip  # compression


"""
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


class Base(object):
    """
    Base class. It holds the encode/decodeB64() functions.

    Defaults:
      encode: .jpg
      use_compression: False
    """
    encode = '.jpg'
    use_compression = False

    def decodeB64(self, b64, depth):
        """base64 to OpenCV"""
        ii = base64.b64decode(b64)
        ii = np.fromstring(ii, dtype=np.uint8)
        img = cv2.imdecode(ii, depth)
        return img

    def encodeB64(self, img):
        """OpenCV to base64"""
        ret, jpeg = cv2.imencode(self.encode, img)
        if not ret:
            print('<<<< error >>>>>>')
        # jpeg = img.tobytes()
        b64 = base64.b64encode(jpeg)
        return b64


class BagReader(Base):
    """
    """
    def load(self, filename):
        """
        Given a filename, it opens it and returns a dict of the data. Any images
        are automatically base64 decoded.
        """
        try:
            if self.use_compression:
                with gzip.open(filename, 'r') as f:
                    data = json.load(f)
            else:
                with open(filename, 'r') as f:
                    data = json.load(f)

            for key in data['b64keys']:
                tmp = []
                for b64, datestamp in data[key]:
                    img = self.decodeB64(b64, 1)  # not sure depth is working
                    tmp.append((img, datestamp))
                data[key] = tmp

        except Exception as e:
            print('Error reading file: {}'.format(filename))
            print(e)
            raise

        return data


class BagWriter(Base):
    """
    """

    def __init__(self):
        self.clear()

    def __del__(self):
        pass

    def stringify(self, keys):
        """
        Images need to be converted to base64 for saving.

        keys: key name or array of key names
        return: None
        """
        if type(keys) is list:
            # print('list', keys)
            for key in keys:
                self.data['b64keys'].append(key)
        elif type(keys) is str:
            # print('str', keys)
            self.data['b64keys'].append(keys)
        else:
            raise Exception('Bag::stringify, invalid input: {}'.format(keys))

    def push(self, key, data):
        """
        Saves data with timestamp. If data is in b64keys (it is an image), then
        it is base64 encoded before saved. All data is saved as: (data, timestamp)

        key: dict key name, if not found, Exception is thrown
        data: data to be saved
        return: None
        """
        if key in self.data:
            # have to convert images (binary) to strings
            if key in self.data['b64keys']:
                data = self.encodeB64(data)

            timestamp = time.time()
            self.data[key].append((data, timestamp))
        else:
            raise Exception('Bag::push, Invalid key: {}'.format(key))

    def clear(self):
        """
        Clears and resets everything.
        """
        self.data = {}
        self.data['b64keys'] = []

    def open(self, topics):
        """
        Set topic keys for writing
        """
        self.clear()
        for key in topics:
            self.data[key] = []

    def write(self, filename):
        """
        Once you write a bag, it is written to disk and the data is cleared
        """
        if self.data == {}:
            return

        if self.use_compression:
            with gzip.open(filename, 'wb') as f:
                # json.dump(self.data, f)
                s = json.dumps(self.data).encode('utf8')
                f.write(s)
        else:
            with open(filename, 'wb') as f:
                # json.dump(self.data, f)
                s = json.dumps(self.data).encode('utf8')
                f.write(s)

        self.clear()

    def size(self):
        """
        Returns dict with the length of data for each key.

        size() -> {'key 1': length, 'key 2': length, ...}
        """
        ret = {}

        for key in self.data.keys():
            ret[key] = len(self.data[key])

        return ret

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
