#!/usr/bin/env python


import cv2
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import time
import argparse
from opencvutils.video import Camera

# threaded version
# http://stackoverflow.com/questions/12650238/processing-simultaneous-asynchronous-requests-with-python-basehttpserver

# not sure flask is any better:
# https://blog.miguelgrinberg.com/post/video-streaming-with-flask


def compress(orig, comp):
	return float(orig) / float(comp)


class mjpgServer(BaseHTTPRequestHandler):
	"""

	"""
	cam = None

	def do_GET(self):
		print 'connection from:', self.address_string()
		if self.path.find('.mjpg') > 0:
			self.send_response(200)
			self.send_header(
				'Content-type',
				'multipart/x-mixed-replace; boundary=--jpgboundary'
			)
			self.end_headers()

			if self.cam is None:
				print 'Error, you need to initialize the camera first'
				return

			capture = self.cam

			while True:
				ret, img = capture.read()
				if not ret:
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
			# pt = self.server.server_address[1]
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<h1>http://{0!s}:{1!s}</h1>'.format(*self.server.server_address))
			self.wfile.write('<img src="http://{0!s}:{1!s}/camera.mjpg"/>'.format(*self.server.server_address))
			self.wfile.write('<p>{0!s}</p>'.format((self.version_string())))
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
	parser.add_argument('-p', '--port', help='port, default is 9000', type=int, default=9000)
	parser.add_argument('-c', '--camera', help='set opencv camera number, ex. -c 1', type=int, default=0)
	parser.add_argument('-t', '--type', help='set type of camera: cv or pi, ex. -t pi', default='cv')
	parser.add_argument('-s', '--size', help='set size', nargs=2, type=int, default=(320, 240))

	args = vars(parser.parse_args())
	args['size'] = (args['size'][0], args['size'][1])
	return args


def main():
	args = handleArgs()
	print args['size']

	try:
		camera = Camera()  # need to figure a clean way to pass this ... move switching logic here?
		camera.init(cameraNumber=0, win=args['size'])
		mjpgServer.cam = camera

		# server = HTTPServer((gethostname(), args['port']), mjpgServer)
		server = HTTPServer(('0.0.0.0', args['port']), mjpgServer)
		print "server started"
		server.serve_forever()

	except KeyboardInterrupt:
		print 'main interrupt'
		server.socket.close()


if __name__ == '__main__':
	main()
