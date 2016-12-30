#!/usr/bin/env python
#
#
# copyright Kevin Walchko
# 29 July 2014
#

from __future__ import print_function
import cv2
import pygecko.lib.ZmqClass as zmq
from opencvutils.video import Camera


class CameraDisplayClient(object):
	def run(self, topic, hostinfo):
		# s = zmq.SubBase64(topics=topic, connect_to=hostinfo)
		s = zmq.Sub(topics=topic, connect_to=hostinfo)
		while True:
			# msg_miss = 1
			try:
				tp, msg = s.recvB64()
				if not msg:
					pass
				elif 'image' in msg:
					im = msg['image']
					cv2.imshow('Camera', im)
					key = cv2.waitKey(10)
					if key == ord('q'):
						break

			except (IOError, EOFError):
				print('[-] Connection gone .... bye')
				break

		s.close()


class LocalCamera(object):
	"""
	More of the same?
	"""
	def __init__(self, args):
		if args['window']: size = args['window']
		else: size = (640, 480)

		if args['file']: self.save = args['file']
		else: self.save = 'video.mp4'

		self.width = int(size[0])
		self.height = int(size[1])
		self.camera = int(args['camera'])

	def run(self):

		# Source: 0 - built in camera  1 - USB attached camera
		cap = Camera()
		cap.init(self.camera, (self.width, self.height))

		# create a video writer to same images
		sv = Camera.SaveVideo()

		print('Press q - quit   SPACE - grab image  s - save video')

		save = False

		while(True):
			# Capture frame-by-frame
			ret, frame = cap.read()

			if ret is True:
				# Display the resulting frame
				cv2.imshow('frame', frame)

				if save:
					sv.write(frame)

			key = cv2.waitKey(10)
			if key == ord('q'):
				break
			elif key == ord(' '):
				print('Grabbing picture')
			elif key == ord('s'):
				save = not save
				if save:
					sv.start(self.save, (self.width, self.height))
				else:
					sv.release()

				print('Saving video: ' + str(save))

		# When everything done, release the capture
		cap.release()
		sv.release()
		cv2.destroyAllWindows()


if __name__ == '__main__':
	client = CameraDisplayClient()
	client.run('image_color', ('localhost', 9000))
