##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################
# import pickle
# from pygecko.transport.protocols import Pickle
from pygecko.messages import image_st
# from pygecko.messages import Joystick
# import numpy as np

try:
    import cv2

    def Image_st(img, compression=None):
        """
        Helper function to create a message from an image and optionally use
        compression. Compression methods are dependant on what libraries were
        compiled at build time for OpenCV.
        """
        if compression:
            compressed = True
            data = cv2.imencode(compression, img)[1]
        else:
            compressed = False
            data = img.tobytes()

        return image_st(img.shape, data, compressed)

except ImportError:

    def Image_st(img, compression=None):
        raise Exception("Image_st: cv2 not installed")


# def image2msg(img, compressed=False, handler=Pickle):
#     if compressed:
#         # import cv2
#         # import msgpack
#         # jpg = cv2.imencode('.jpg', img)[1]
#         m = handler.dumps(img.tobytes())
#         msg = Image(img.shape, m, True)
#     else:
#         msg = Image(img.shape, img.tobytes(), False)
#     return msg
#
#
# def msg2image(msg, handler=Pickle):
#     raw = msg.bytes
#     if msg.compressed:
#         raw = handler.loads(msg.bytes)
#     img = np.frombuffer(raw, dtype=np.uint8)
#     img = img.reshape(msg.shape)
#     return img


# def msg2image(msg):
#     raw = msg.bytes
#     if msg.compressed:
#         # import cv2
#         # import msgpack
#         # raw = nparr = np.fromstring(msg.bytes, np.uint8)
#         # img = np.frombuffer(raw, dtype=np.uint8)
#         # if len(msg.shape) == 3:
#         #     img = cv2.imdecode(img, cv2.IMREAD_COLOR)  # cv2.IMREAD_COLOR = 1
#         # else:
#         #     cv2.imdecode(img, cv2.IMREAD_GRAYSCALE)  # cv2.IMREAD_GRAYSCALE = 0
#         raw = handler.loads(msg.bytes)
#     #     img = np.frombuffer(raw, dtype=np.uint8)
#     #     img = img.reshape(msg.shape)
#     # else:
#     #     img = np.frombuffer(msg.bytes, dtype=np.uint8)
#     #     img = img.reshape(msg.shape)
#
#     img = np.frombuffer(raw, dtype=np.uint8)
#     img = img.reshape(msg.shape)
#     return img


# def msg2ps4(msg):
#     return Joystick(0,0,0)
#
#
# def ps42msg(joy):
#     return Joystick(0,0,0)
