#!/usr/bin/env python
#
# Kevin J. Walchko 11 Nov 2014
#

from __future__ import print_function
from __future__ import division
import pygecko.lib.ZmqClass as zmq
from pygecko.lib import Messages as Msg
import multiprocessing as mp
# import logging
import datetime as dt
import cv2
import argparse
from opencvutils.video import Camera
import time

# --- topics --------------------------------------------------------------
#   image_raw - raw data from the camera driver, possibly Bayer encoded
#   image            - monochrome, distorted
#   image_color      - color, distorted
#   image_rect       - monochrome, rectified
#   image_rect_color - color, rectified


# class RobotCameraServer(object):
class RobotCameraServer(mp.Process):
	"""
	Streams camera images as fast as possible
	"""
	def __init__(self, host="0.0.0.0", port='9100', camera_num=0):
		mp.Process.__init__(self)
		self.epoch = dt.datetime.now()
		self.host = host
		self.port = port
		self.camera_num = camera_num
		# logging.basicConfig(level=logging.INFO)
		# self.logger = logging.getLogger('robot')

		# self.epoch = dt.datetime.now()

	# def start(self):
	# 	self.run()
	#
	# def join(self):
	# 	pass

	def run(self):
		# self.logger.info(str(self.name) + '[' + str(self.pid) + '] started on ' + str(self.host) + ':' + str(self.port) + ', Daemon: ' + str(self.daemon))
		# pub = zmq.PubBase64((self.host, self.port))
		pub = zmq.Pub((self.host, self.port))
		camera = Camera()
		camera.init(cameraNumber=self.camera_num, win=(640, 480))

		# self.logger.info('Openned camera: ' + str(self.camera_num))

		try:
			while True:
				ret, frame = camera.read()
				jpeg = cv2.imencode('.jpg', frame)[1]  # jpeg compression
				msg = Msg.Image(jpeg)
				pub.pubB64('image_color', msg)
				# print '[*] frame: %d k   jpeg: %d k'%(frame.size/1000,len(jpeg)/1000)
				time.sleep(0.01)

		except KeyboardInterrupt:
			print('Ctl-C ... exiting')
			return


# set up and handle command line args
def handleArgs():
	parser = argparse.ArgumentParser(description='A simple zero MQ pub/sub for a camera Example: RobotCameraServer pub 192.168.10.22 8080')
	# parser.add_argument('info', nargs=3, help='pub or sub, hostname, port; example: pub 10.1.1.1 9333', default=['pub','localhost','9000'])
	# parser.add_argument('-a', '--address', help='host address', default='localhost')
	# parser.add_argument('-p', '--port', help='port', default='9100')
	parser.add_argument('-f', '--file', help='file name to save video to')
	# parser.add_argument('-g', '--host', nargs=2, help='size of pattern, for example, -s 6 7', required=True)
	# parser.add_argument('-p', '--path', help='location of images to use', required=True)
	# parser.add_argument('-d', '--display', help='display images', default=True)
	parser.add_argument('-p', '--pub', nargs=2, help='publish images to addr:port, ex. pub 10.1.1.1 9000')
	parser.add_argument('-s', '--sub', nargs=2, help='subscribe to images at addr:port, ex. sub 10.1.1.1 9000')
	parser.add_argument('-l', '--local', help='display images to screen', action='store_true')
	parser.add_argument('-w', '--window', nargs=2, help='set window size, ex. -w 640 480')
	parser.add_argument('-c', '--camera', help='set camera number, ex. -c 1', type=int, default=0)
	# parser.add_argument('-f', '--file', help='if local, save images to file')

	args = vars(parser.parse_args())
	return args


# def main():
# 	print('Hello cowboy!')
#
#
# if __name__ == "__main__":
# 	main()
