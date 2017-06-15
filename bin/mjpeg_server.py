#!/usr/bin/env python

import cv2
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
import time
import argparse
from opencvutils import Camera
import socket as Socket
# import errno

# threaded version
# http://stackoverflow.com/questions/12650238/processing-simultaneous-asynchronous-requests-with-python-basehttpserver

# not sure flask is any better:
# https://blog.miguelgrinberg.com/post/video-streaming-with-flask

#``mjpeg_server``
#	* only handles one connection at a time ... make threaded?
#	* sometimes the video stream is slow to load, but then it works fine
#	* handle client disconnect (broken pipe - 32) better


def compress(orig, comp):
	return float(orig) / float(comp)


class mjpgServer(BaseHTTPRequestHandler):
	"""
	A simple mjpeg server that either publishes images directly from a camera
	or republishes images from another pygecko process.
	"""

	cam = None
	cameratype = 'cv'
	host = None
	win = (640, 480)

	def __del__(self):
		if self.cam:
			self.cam.close()
		self.cam = None
		print 'Exiting mjpgServer'

	def setUpCamera(self):
		"""
		cv - camera number, usually 0
		pi - set to True
		"""
		print 'window size:', self.win
		if self.cameratype == 'pi':
			self.cam = Camera('pi')
			self.cam.init(win=self.win)
		elif self.cameratype == 'cv':
			self.cam = Camera('cv')
			self.cam.init(cameraNumber='cv', win=self.win)

		else:
			raise Exception('Error, you must specify "cv" or "pi" for camera type')

		time.sleep(3)

	def do_GET(self):
		print 'connection from:', self.address_string()

		if self.path == '/mjpg':
			print 'mjpg'
			self.send_response(200)
			self.send_header(
				'Content-type',
				'multipart/x-mixed-replace; boundary=--jpgboundary'
			)
			self.end_headers()

			while True:
				if self.cam:
					# print 'grab image'
					ret, img = self.cam.read()
				else:
					# print 'setupcamera()'
					self.setUpCamera()
					ret = False
				# ret, img = self.getImage()
				if not ret:
					# print 'crap'
					time.sleep(1)
					continue

				ret, jpg = cv2.imencode('.jpg', img)
				# print 'Compression ratio: %d4.0:1'%(compress(img.size,jpg.size))
				self.wfile.write("--jpgboundary")
				self.send_header('Content-type', 'image/jpeg')
				# self.send_header('Content-length',str(tmpFile.len))
				self.send_header('Content-length', str(jpg.size))
				self.end_headers()
				self.wfile.write(jpg.tostring())
				time.sleep(0.05)

		elif self.path == '/':
			ip = self.host[0]
			port = self.host[1]

			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<h1>{0!s}:{1!s}</h1>'.format(ip, port))
			self.wfile.write('<img src="http://{}:{}/mjpg"/>'.format(ip, port))
			self.wfile.write('<p>{0!s}</p>'.format((self.version_string())))
			self.wfile.write('</p></ul>')
			self.wfile.write('<p>This only handles one connection at a time</p>')
			self.wfile.write('</body></html>')

		else:
			print 'error', self.path
			self.send_response(404)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<h1>{0!s} not found</h1>'.format(self.path))
			self.wfile.write('</body></html>')


def handleArgs():
	parser = argparse.ArgumentParser(description='A simple mjpeg server Example: mjpeg-server -p 8080 --camera 4')
	parser.add_argument('-p', '--port', help='local publisher port, default is 9000', type=int, default=9000)
	# parser.add_argument('-c', '--camera', help='set opencv camera number, ex. -c 1', type=int, default=0)
	parser.add_argument('-t', '--type', help='set type of camera: cv or pi, ex. -t pi', default='cv')
	parser.add_argument('-s', '--size', help='set size', nargs=2, type=int, default=(640, 480))
	# parser.add_argument('-r', '--remote', help='remote host image subscription info, hostname/ip port, ex: 1.2.3.4 9000', nargs=2, default=('0.0.0.0', 9000))

	args = vars(parser.parse_args())
	args['size'] = (args['size'][0], args['size'][1])
	# args['remote'] = (args['remote'][0], args['remote'][1])
	return args


def main():
	args = handleArgs()

	# figure out host info
	hostname = Socket.gethostname()
	if hostname.find('.local') == -1:
		hostname += '.local'
	ip = Socket.gethostbyname(hostname)
	hostinfo = (ip, args['port'])

	try:
		mjpgServer.topic = 'image_color'
		mjpgServer.cameratype = 'pi'
		mjpgServer.host = hostinfo
		mjpgServer.win = args['size']
		server = HTTPServer(hostinfo, mjpgServer)
		print "server started on: {}:{}".format(ip, args['port'])
		server.serve_forever()

	except KeyboardInterrupt:
		print 'KeyboardInterrupt'
		server.socket.close()
		exit(0)


if __name__ == '__main__':
	main()
