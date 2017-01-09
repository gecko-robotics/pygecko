#!/usr/bin/env python

# import simplejson as json
import base64
import cv2
import timeit
from pygecko.lib import Messages as Msg
import numpy as np
# import math
# import time
from test import Image, serialize, deserialize

loop_num = 100


def time_image():
	im = Image()
	save = np.random.randint(0, 255, size=(640, 480))
	im.img = save

	msg = serialize(im)
	deserialize(msg)


def pygecko_image():
	frame = np.random.randint(0, 255, size=(640, 480))
	jpeg = cv2.imencode('.jpg', frame)[1]
	b64 = base64.b64encode(jpeg)
	m = Msg.Image(b64)
	m = Msg.serialize(m)
	m = Msg.deserialize(m)
	# print m
	ii = base64.b64decode(m['image'])
	ii = np.fromstring(ii, dtype=np.uint8)
	cv2.imdecode(ii, 0)


print 'old dict', timeit.timeit("pygecko_image()", "from __main__ import pygecko_image", number=loop_num)
print 'new classes', timeit.timeit("time_image()", "from __main__ import time_image", number=loop_num)
