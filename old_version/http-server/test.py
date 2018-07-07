#!/usr/bin/env python

from __future__ import division, print_function
# import multiprocessing as mp
import time
import bjoern
import cv2


class Camera(object):
	def __init__(self, src):
		self.cam = cv2.VideoCapture(src)

	def read(self):
		ret = None
		ok, img = self.cam.read()
		if ok:
			img2 = cv2.resize(img, dsize=(320, 240))
			ok, jpeg = cv2.imencode('.jpg', img2)
			if ok:
				ret = jpeg.tostring()
		return ret

# urls = {'/': "hello world", '/greet': "hi user!"}
cam = Camera(0)


def app(environ, start_response):
	print(environ)
	try:
		# response_body = urls[environ['PATH_INFO']]
		# if environ['PATH_INFO'] == '/mjpeg':
		response_body = cam.read()
		status = '200 OK'
		response_headers = [
			('Content-Type', 'image/jpeg'),
			('Content-Length', str(len(response_body)))
		]
		# start_response(status, response_headers)
		start_response(status, response_headers)
		# yield [response_body]

	except Exception as e:
		print(e)
		status = '404 OK'
		response_body = 'File not found'
		response_headers = [
			('Content-Type', 'text/plain'),
			('Content-Length', str(len(response_body)))
		]
		start_response(status, response_headers)

	# print('>>', response_body)
	# start_response(status, response_headers)
	return [response_body]


bjoern.listen(app, "localhost", 8000, True)
bjoern.run()
