#!/usr/bin/env python

from __future__ import print_function
from pygecko.Vision import RobotCameraServer as CameraServer
from pygecko.navigation import Navigation
from pygecko.Audio import SoundServer





def main():
	cs = CameraServer('localhost', 9000)
	nav = Navigation('localhost', 9001)
	aud = SoundServer('localhost', 9002)

	print('start processes')
	nav.start()
	aud.start()
	cs.start()

	print('join processes')
	# cs.join()
	nav.join()
	aud.join()

if __name__ == "__main__":
	main()
