#!/usr/bin/env python

import cv2
# from opencvutils.video import Camera
from flask import Flask
# from flask import render_template
from flask import Response
import logging

cam = cv2.VideoCapture(0)
cam.set(3, 320)  # width
cam.set(4, 240)  # height

app = Flask(__name__)

page = """
<html>
	<body>
		<h1>video</h1>
		<img src="http://127.0.0.1:5000/mjpeg" alt="mjpeg" style="width:320px;height:240px;">
	</body>
</html>
"""


@app.route('/')
def root():
	# disable logging in Flask (it's enabled by default)
	log = logging.getLogger('werkzeug')
	log.setLevel(logging.ERROR)
	return Response(page, mimetype='text/html'), 200


def video(fmt='jpeg'):
	# cam = cv2.VideoCapture(0)
	# cam.set(3, 320)  # width
	# cam.set(4, 240)  # height

	while True:
		ret, frame = cam.read()
		# print 'frame', ret, frame.shape, frame.size
		# ret, frame = cv2.imencode('.jpg', frame)
		ret, frame = cv2.imencode('.' + fmt, frame)
		# print 'jpeg', frame.size
		yield(b'--boundary\r\n' +
			# b'Content-Type: image/jpeg\r\n' +
			b'Content-Type: image/{}\r\n'.format(fmt) +
			b'Content-length: ' + str(frame.size) + b'\r\n\r\n' +
			frame.tostring() + b'\r\n')


@app.route('/mjpeg')
def mjpeg():
	return Response(video(), mimetype='multipart/x-mixed-replace; boundary=boundary')


@app.errorhandler(404)
def page_not_found(error):
	# app.logger.error('Page not found: %s', (request.path))
	print error
	# return render_template('404.htm'), 404
	return 'oops', 404


@app.errorhandler(Exception)
def unhandled_exception(e):
	print 'Exception:', e
	exit()


if __name__ == '__main__':
	app.run()
