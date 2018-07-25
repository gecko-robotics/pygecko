#!/usr/bin/env python3

"""
So this is sort of a copy of roslaunch
"""

import sys
sys.path.append("../")
from pygecko.multiprocessing import GeckoProcess
import multiprocessing as mp
import time

class Test(GeckoProcess):
	def __init__(self, ps):
		GeckoProcess.__init__(self, ps)

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
    # if you read in a json file
	ps = {
		# file, function, args
		'processes': [
			('process', 'runable_process', {'a':1, 'b':2},),
			('process', 'runable_process',),
			('process', 'runable_process', None,),
		]
	}

	g = Test(ps)
	g.loop()
