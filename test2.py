#!/usr/bin/env python

from __future__ import division, print_function
# import multiprocessing as mp
import time
import bjoern
# import cv2
# import time
import falcon
from jinja2 import Environment
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import Scatter, Figure, Layout, Histogram2dContour, Contours, Marker
import numpy as np


class Main(object):
	# def __init__(self):
	# 	pp = plot([Scatter(x=[1, 2, 3], y=[3, 1, 6])], show_link=False, include_plotlyjs=True, output_type='div')
	# 	# x = np.random.randn(2000)
	# 	# y = np.random.randn(2000)
	# 	# nn = plot(
	# 	# 	[
	# 	# 		Histogram2dContour(x=x, y=y, contours=Contours(coloring='heatmap')),
	# 	# 		Scatter(x=x, y=y, mode='markers', marker=Marker(color='white', size=3, opacity=0.3))
	# 	# 	],
	# 	# 	show_link=False, include_plotlyjs=True, output_type='div')
	#
	# 	fig = {
	# 	  "data": [
	# 		{
	# 		  "values": [16, 15, 12, 6, 5, 4, 42],
	# 		  "labels": [
	# 			"US",
	# 			"China",
	# 			"European Union",
	# 			"Russian Federation",
	# 			"Brazil",
	# 			"India",
	# 			"Rest of World"
	# 		  ],
	# 		  "domain": {"x": [0, .48]},
	# 		  "name": "GHG Emissions",
	# 		  "hoverinfo":"label+percent+name",
	# 		  "hole": .4,
	# 		  "type": "pie"
	# 		},
	# 		{
	# 		  "values": [27, 11, 25, 8, 1, 3, 25],
	# 		  "labels": [
	# 			"US",
	# 			"China",
	# 			"European Union",
	# 			"Russian Federation",
	# 			"Brazil",
	# 			"India",
	# 			"Rest of World"
	# 		  ],
	# 		  "text":"CO2",
	# 		  "textposition":"inside",
	# 		  "domain": {"x": [.52, 1]},
	# 		  "name": "CO2 Emissions",
	# 		  "hoverinfo":"label+percent+name",
	# 		  "hole": .4,
	# 		  "type": "pie"
	# 		}],
	# 	  "layout": {
	# 			"title":"Global Emissions 1990-2011",
	# 			"annotations": [
	# 				{
	# 					"font": {
	# 						"size": 20
	# 					},
	# 					"showarrow": False,
	# 					"text": "GHG",
	# 					"x": 0.20,
	# 					"y": 0.5
	# 				},
	# 				{
	# 					"font": {
	# 						"size": 20
	# 					},
	# 					"showarrow": False,
	# 					"text": "CO2",
	# 					"x": 0.8,
	# 					"y": 0.5
	# 				}
	# 			]
	# 		}
	# 	}
	# 	nn = plot(fig, show_link=False, include_plotlyjs=True, output_type='div')
	#
	# 	html = "<!DOCTYPE html><html><head></head><body>{{ title }} {{ two }}</body></html>"
	# 	self.html = Environment().from_string(html).render(title=pp, two=nn)

	def on_get(self, req, resp):
		"""Handles GET requests"""

		pp = plot([Scatter(x=[1, 2, 3], y=[3, 1, 6])], show_link=False, include_plotlyjs=True, output_type='div')
		# x = np.random.randn(2000)
		# y = np.random.randn(2000)
		# nn = plot(
		# 	[
		# 		Histogram2dContour(x=x, y=y, contours=Contours(coloring='heatmap')),
		# 		Scatter(x=x, y=y, mode='markers', marker=Marker(color='white', size=3, opacity=0.3))
		# 	],
		# 	show_link=False, include_plotlyjs=True, output_type='div')

		fig = {
		  "data": [
			{
			  "values": [16, 15, 12, 6, 5, 4, 42],
			  "labels": [
				"US",
				"China",
				"European Union",
				"Russian Federation",
				"Brazil",
				"India",
				"Rest of World"
			  ],
			  "domain": {"x": [0, .48]},
			  "name": "GHG Emissions",
			  "hoverinfo":"label+percent+name",
			  "hole": .4,
			  "type": "pie"
			},
			{
			  "values": [27, 11, 25, 8, 1, 3, 25],
			  "labels": [
				"US",
				"China",
				"European Union",
				"Russian Federation",
				"Brazil",
				"India",
				"Rest of World"
			  ],
			  "text":"CO2",
			  "textposition":"inside",
			  "domain": {"x": [.52, 1]},
			  "name": "CO2 Emissions",
			  "hoverinfo":"label+percent+name",
			  "hole": .4,
			  "type": "pie"
			}],
		  "layout": {
				"title":"Global Emissions 1990-2011",
				"annotations": [
					{
						"font": {
							"size": 20
						},
						"showarrow": False,
						"text": "GHG",
						"x": 0.20,
						"y": 0.5
					},
					{
						"font": {
							"size": 20
						},
						"showarrow": False,
						"text": "CO2",
						"x": 0.8,
						"y": 0.5
					}
				]
			}
		}
		nn = plot(fig, show_link=False, include_plotlyjs=True, output_type='div')

		html = "<!DOCTYPE html><html><head></head><body>{{ title }} {{ two }}</body></html>"
		self.html = Environment().from_string(html).render(title=pp, two=nn)

		# resp.media = str(time.time())
		resp.status = falcon.HTTP_200
		resp.content_type = 'text/html'
		resp.body = self.html
		# resp.data = self.html.encode('utf-8')
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
