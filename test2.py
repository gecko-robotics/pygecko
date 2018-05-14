#!/usr/bin/env python

from __future__ import division, print_function
# import multiprocessing as mp
import time
import bjoern
import cv2
import time
import falcon
from jinja2 import Environment


class Main(object):
	def __init__(self):
		html = "<!DOCTYPE html><html><head><title>{{ title }}</title></head><body>Hello.</body></html>"
		self.html = Environment().from_string(html).render(title='Hellow Gist from GutHub')

	def on_get(self, req, resp):
		"""Handles GET requests"""

		# resp.media = str(time.time())
		resp.data = self.html.encode('utf-8')
		# print(dir(req))
		# print('-'*30)
		# print(resp)

class QuoteResource(object):
	def on_get(self, req, resp):
		"""Handles GET requests"""
		quote = {
			'quote': (
				"I've always been more interested in "
				"the future than in the past."
			),
			'author': 'Grace Hopper'
		}

		resp.media = quote


api = falcon.API()
api.add_route('/quote', QuoteResource())
api.add_route('/', Main())

try:
	bjoern.listen(api, "localhost", 8000, True)
	bjoern.run()
except KeyboardInterrupt:
	pass
