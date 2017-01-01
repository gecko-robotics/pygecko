#!/usr/bin/env python


import cv2
import pygecko.lib.ZmqClass as zmq
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import time
import argparse
from opencvutils.video import Camera
import socket as Socket
import errno

# threaded version
# http://stackoverflow.com/questions/12650238/processing-simultaneous-asynchronous-requests-with-python-basehttpserver

# not sure flask is any better:
# https://blog.miguelgrinberg.com/post/video-streaming-with-flask


def compress(orig, comp):
	return float(orig) / float(comp)


class mjpgServer(BaseHTTPRequestHandler):
	"""
	A simple mjpeg server that either publishes images directly from a camera
	or republishes images from another pygecko process.
	"""

	cam = None
	sub = None
	topic = None
	hostinfo = None
	ip = None
	hostname = None

	def setUpCamera(self, cv=None, pi=None, win=(320, 240)):
		"""
		cv - camera number, usually 0
		pi - set to True
		"""
		if pi:
			self.cam = Camera('pi')
			self.cam.init(win=win)
		elif cv:
			self.cam = Camera('cv')
			self.cam.init(cameraNumber=cv, win=win)

		else:
			raise Exception('Error, you must specify "cv" or "pi" for camera type')

	def getImage(self):
		if self.cam:
			print 'cam'
			return self.cam.read()

		elif self.sub:
			# print 'sub'
			_, msg = self.sub.recvB64()
			if msg:
				return True, msg['image']
			else:
				return False, None
		else:
			print 'sub init'
			if not self.topic or not self.hostinfo:
				raise Exception('Error, you must either setup camera or setup subscriber topic/hostinfo')
			self.sub = zmq.Sub(topics=self.topic, connect_to=self.hostinfo)
			return False, None

	# def do_HEAD(s):
	# 	print 'do_HEAD'
	# 	s.send_response(200)
	# 	s.send_header("Content-type", "text/html")
	# 	s.end_headers()

	def do_GET(self):
		print 'connection from:', self.address_string()

		if self.ip is None or self.hostname is None:
			self.hostname = Socket.gethostname()
			self.ip = Socket.gethostbyname(Socket.gethostname())

		if self.path == '/mjpg':
			self.send_response(200)
			self.send_header(
				'Content-type',
				'multipart/x-mixed-replace; boundary=--jpgboundary'
			)
			self.end_headers()

			while True:
				# ret, img = capture.read()
				ret, img = self.getImage()
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
			# hn = self.server.server_address[0]
			port = self.server.server_address[1]
			ip = self.ip
			hostname = self.ip

			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<h1>{0!s}[{1!s}]:{2!s}</h1>'.format(hostname, ip, port))
			self.wfile.write('<img src="http://{}:{}/mjpg"/>'.format(ip, port))
			self.wfile.write('<p>{0!s}</p>'.format((self.version_string())))
			self.wfile.write('<p>The mjpg stream can be accessed directly at:<ul>')
			self.wfile.write('<li><a href="http://{0!s}:{1!s}/mjpg"/>http://{0!s}:{1!s}/mjpg</a></li>'.format(ip, port))
			self.wfile.write('<li><a href="http://{0!s}:{1!s}/mjpg"/>http://{0!s}:{1!s}/mjpg</a></li>'.format(hostname, port))
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
	parser.add_argument('-c', '--camera', help='set opencv camera number, ex. -c 1', type=int, default=0)
	parser.add_argument('-t', '--type', help='set type of camera: cv or pi, ex. -t pi', default='cv')
	parser.add_argument('-s', '--size', help='set size', nargs=2, type=int, default=(320, 240))
	parser.add_argument('-r', '--remote', help='remote host image subscription info, hostname/ip port, ex: 1.2.3.4 9000', nargs=2, default=('0.0.0.0', 9000))

	args = vars(parser.parse_args())
	args['size'] = (args['size'][0], args['size'][1])
	args['remote'] = (args['remote'][0], args['remote'][1])
	return args


def main():
	args = handleArgs()
	# print args['size']

	try:
		mjpgServer.topic = 'image_color'
		mjpgServer.hostinfo = ('zoidberg.local', 9000)
		server = HTTPServer(('0.0.0.0', args['port']), mjpgServer)
		print "server started on port: {}".format(args['port'])
		server.serve_forever()

	except KeyboardInterrupt:
		print 'KeyboardInterrupt'

	server.socket.close()

	# except Exception as e:
	# 	print 'Error', e
	# 	server.socket.close()
	#
	# except Socket.error as e:
	# 	if e.errno == errno.EPIPE:
	# 		print 'broken pipe?'
	# 	else:
	# 		print 'some other socket error'
	#
	# except:
	# 	print 'crap something happened'


if __name__ == '__main__':
	main()
