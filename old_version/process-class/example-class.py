#!/usr/bin/env python

from __future__ import division, print_function
import multiprocessing as mp
import time
from pygecko.gecko import Gecko


class Test(Gecko):
	def __init__(self, ps):
		Gecko.__init__(self, ps)

	def loop(self):
		self.start()

		try:
			while self.event.is_set():
				time.sleep(1)
				for p in mp.active_children():
					print(p.name, p.pid)
				# debugging info here via print or logging or webpage
		except (KeyboardInterrupt, SystemExit):
			# set the kill flag
			self.event.clear()

		finally:
			self.end()


if __name__ == '__main__':
	ps = {
		# file, function, args
		'processes': [
			# ('camera', 'streamer', 8888,),
			# ('camera', 'camera_p', 0,),
			('camera', 'camera_srv', ['a', 'bunch of stuff'],),
			('camera', 'camera_srv', ['a', 'bunch of stuff'],),
			('camera', 'camera_srv', None,),
		]
	}

	g = Test(ps)
	g.loop()
