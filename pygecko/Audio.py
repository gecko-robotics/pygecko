#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
# import os							# run commands and get/use path
# import platform						# determine os
import sys							# ?
# import time							# sleep
import logging						# logging
import multiprocessing as mp		# multiprocess
import lib.zmqclass as zmq
import lib.FileStorage as fs
# import lib.WitInput as wi
from lib.tts import TTS
from lib.chatbot import Chatbot
import speech_recognition as sr


class SoundServer(mp.Process):
	"""
	"""
	# def __init__(self, YAML_FILE, REAL, stdin=os.fdopen(os.dup(sys.stdin.fileno())), host="localhost", port=9200):
	def __init__(self, wit_token, host="localhost", port=9200):
		mp.Process.__init__(self)
		self.host = host
		self.port = port
		logging.basicConfig(level=logging.DEBUG)
		self.logger = logging.getLogger(__name__)

		self.logger.info('soundserver stdin: ' + str(sys.stdin.fileno()))

		self.pub = zmq.Pub((host, port))
		self.sub = zmq.Sub('text', (host, str(port + 1)))

		self.tts = TTS()
		self.chatbot = Chatbot()

		results = """--------------------------
		Sound Server up
		Pub[text out]: %s:%d
		Sub[text in]: %s:%d
		Modules: %d
		--------------------------
		"""
		self.logger.info(results, host, port, host, port + 1, len(self.modules))

	def run(self):
		"""
		Main process run loop
		in: none
		out: none
		"""
		# main loop
		try:
			# self.logger.info(str(self.name)+'['+str(self.pid)+'] started on '+
			# 	str(self.host) + ':' + str(self.port) +', Daemon: '+str(self.daemon))
			loop = True
			while loop:
				# get wit.ai json
				# result = self.input.listenPrompt()
				result = self.input.listen()

				txt = self.chatbot.test(result)

				if txt == 'exit_loop':
					loop = False
				elif txt == 'empty' or not txt:
					self.logger.info('no plugin response')
					continue
				else:
					self.logger.debug('response' + txt)
					self.tts.say(txt)

			self.speak('Good bye ...')

		except KeyboardInterrupt:
			print('{} exiting'.format(__name__))
			raise KeyboardInterrupt


if __name__ == '__main__':
	s = SoundServer()
	s.readPlugins()  # what should I do for this??
	s.start()
	print('bye ...')



# import speech_recognition as sr
#
# def loop(r):
# 	audio = None
# 	ret = ''
#
# 	with sr.Microphone() as source:
# 		# r.adjust_for_ambient_noise(source)
# 		print("Say something!")
# 		# audio = None
# 		audio = r.listen(source, 1.0)
# 
# 	ret = r.recognize_sphinx(audio)
#
# 	print(">>" + ret)
#
# 	if ret == 'quit':
# 		exit()
#
# def main2():
# 	# obtain audio from the microphone
# 	r = sr.Recognizer()
#
# 	while True:
# 		with sr.Microphone() as source:
# 			r.adjust_for_ambient_noise(source)
#
# 		try:
# 			loop(r)
#
# 		except sr.WaitTimeoutError as e:
# 			pass
#
# 		except KeyboardInterrupt as e:
# 			print('Ctrl-c ... bye')
# 			break
