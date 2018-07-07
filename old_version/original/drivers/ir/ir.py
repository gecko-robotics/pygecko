#!/usr/bin/env python

from __future__ import division


class IR(object):
	# i don't think one class for both will work
	IR_ANALOG = 0
	IR_DIGITAL = 1

	# https://www.pololu.com/category/79/sharp-distance-sensors
	# (min_dist, max_dist, min_volt, max_volt)
	SHARP_GP2Y0A02YK0F = (15, 150, 0.4, 2.8, IR_ANALOG)
	SHARP_GP2Y0A21 = (10, 80, 0.4, 2.8, IR_ANALOG)
	SHARP_GP2Y0A41SK0F = (4, 30, 0.4, 2.8, IR_ANALOG)
	SHARP_GP2Y0D810Z0F = (2, 10, 0, 3.3, IR_DIGITAL)

	def __init__(self, model, bits, ttl=3.3):
		# self.min = model[0]
		# self.max = model[1]
		self.model = model
		self.max_adc = 2**bits
		self.ttl = ttl

	def range(self, reading):
		min_dist, max_dist, min_volt, max_volt, digital = self.model
		if digital:
			dist = max_dist
		else:
			dist = (max_dist - min_dist) * reading / self.max_adc

		return dist
