# -*- coding: utf-8 -*-
from __future__ import division, print_function
import time
import cv2
from math import cos, sin
import socket
import errno
import threading


# def streamer(ns, e, port):
# 	serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 	serv.bind((socket.gethostname(), port))
# 	serv.listen(5)
# 	conn, address = serv.accept()
# 	print("Connection from: " + str(address))
# 	while e.is_set():
# 		data = conn.recv(1024).decode()
# 		if not data:
# 			break
# 		print('>', data)
# 		msg = b"""
# 			HTTP/1.1
# 			Content-Type: text/html
#
# 			<html>
# 			<body>
# 			<b>Hello World</b>
# 			</body>
# 			</html>
# 		"""
# 		conn.sendall(msg)
# 		print('> send msg')
# 	conn.close()

def handle(ns, e, conn):
	CRLF = "\r\n"
	start = time.time()
	try:
		while e.is_set():
			# serv.settimeout(0.01)
			data = conn.recv(1024).decode()
			if not data:
				continue
			print('> data recv:\n', data)
			msg = "HTTP/1.1 200 OK" + CRLF
			msg += "Access-Control-Allow-Origin: *" + CRLF
			msg += "Connection: keep-alive" + CRLF
			# msg += "Connection: close" + CRLF
			msg += "Server: mjpeg server" + CRLF
			# msg += "Cache-Control: no-cache" + CRLF
			# msg += "Cache-Control: private" + CRLF
			msg += "Cache-Control: no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0" + CRLF
			msg += "Pragma: no-cache" + CRLF
			msg += "Expires: Mon, 3 Jan 2000 12:34:56 GMT" + CRLF
			msg += "Content-Type: multipart/x-mixed-replace; boundary=jpgboundary" + CRLF
			# msg = msg.decode('utf-8')
			conn.sendall(msg)
			print('> send\n', msg)
			while e.is_set():
				# data = conn.recv(1024).decode()
				# if data:
					# print('data Rx:', data)
				if ns.img_str:
					msg = "--jpgboundary" + CRLF
					msg += "X-Timestamp: {}".format(time.time() - start) + CRLF
					msg += "Content-type: image/jpeg" + CRLF
					msg += "Content-length: " + str(len(ns.img_str)) + CRLF + CRLF
					# msg = "--jpgboundary" + CRLF
					# msg += ns.img_str
					# msg += CRLF + CRLF
					# msg = msg.decode('utf-8')  # no py3
					conn.sendall(msg)
					conn.sendall(ns.img_str)
					print(msg)
					print('>> send image')
				time.sleep(0.03)

				data = conn.recv(1024).decode()
				if data:
					print('data Rx:', data)

	except socket.error as err:
		print(err)
		if isinstance(err.args, tuple):
			if err[0] == errno.EPIPE:
				print('Remote disconnect')
				# e.clear()

	conn.close()


def streamer(ns, e, port):
	serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
	serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serv.bind((socket.gethostname(), port))
	serv.listen(15)

	while e.is_set():
		conn, address = serv.accept()
		print("Connection from: " + str(address))
		threading.Thread(target=handle, args=(ns, e, conn,)).start()
	#
	# try:
	# 	while e.is_set():
	# 		# serv.settimeout(0.01)
	# 		data = conn.recv(1024).decode()
	# 		if not data:
	# 			continue
	# 		print('> data recv:\n', data)
	# 		msg = "HTTP/1.1 200 OK" + CRLF
	# 		msg += "Connection: keep-alive" + CRLF
	# 		msg += "Server: mjpeg server" + CRLF
	# 		msg += "Cache-Control: no-cache" + CRLF
	# 		msg += "Cache-Control: private" + CRLF
	# 		msg += "Content-Type: multipart/x-mixed-replace; boundary=--jpgboundary" + CRLF
	# 		# msg = msg.decode('utf-8')
	# 		conn.sendall(msg)
	# 		print('> send\n', msg)
	# 		while e.is_set():
	# 			# data = conn.recv(1024).decode()
	# 			# if data:
	# 				# print('data Rx:', data)
	# 			if ns.img_str:
	# 				msg = b"--jpgboundary" + CRLF
	# 				msg += "Content-type: image/jpeg" + CRLF
	# 				msg += "Content-length: " + str(len(ns.img_str)) + CRLF + CRLF
	# 				# msg += ns.img_str
	# 				# msg += CRLF + CRLF
	# 				# msg = msg.decode('utf-8')  # no py3
	# 				conn.sendall(msg)
	# 				conn.sendall(ns.img_str)
	# 				# print(msg)
	# 				print('>> send image')
	# 			time.sleep(0.03)
	# except socket.error as err:
	# 	print(err)
	# 	if isinstance(err.args, tuple):
	# 		if err[0] == errno.EPIPE:
	# 			print('Remote disconnect')
	# 			e.clear()
	#
	# conn.close()


class Camera(object):
	def __init__(self, src):
		self.cam = cv2.VideoCapture(src)

	def read(self):
		ret = None
		ok, img = self.cam.read()
		if ok:
			img2 = cv2.resize(img, dsize=(320, 240))
			ok, jpeg = cv2.imencode('.jpg', img2)
			if ok:
				ret = jpeg.tostring()
		return ret


def camera_p(ns, e, vidsrc):
	cam = Camera(vidsrc)
	while e.is_set():
		try:
			ns.img_str = cam.read()
			time.sleep(0.033)
		except:
			continue
	print('Exiting camera_p ...')


def camera_srv(ns, e, args=None):
	"""
	for some reason, this sees ctrl-C kill exception instead of ONLY the
	main loop. put a bare except to ingnore ctrl-C
	"""
	if args:
		print('Also got:', args)

	while e.is_set():
		try:
			# if ns.img_str:
			# 	print('image len:', len(ns.img_str))
			# for i in range(200):
			# 	a = cos(i)*sin(i)
			time.sleep(0.5)
		except:
			continue
	print('Exiting camera_srv ...')
