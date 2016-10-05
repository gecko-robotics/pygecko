#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
import os							# run commands and get/use path
import platform						# determine os
import sys							# ?
# import time							# sleep
import logging						# logging
import multiprocessing as mp		# multiprocess
import lib.zmqclass as zmq
import lib.FileStorage as fs
# import lib.WitInput as wi
from lib.tts import TTS


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
		# self.os = platform.system()  # why?

		self.logger.info('soundserver stdin: ' + str(sys.stdin.fileno()))

		self.pub = zmq.Pub((host, port))
		self.sub = zmq.Sub('text', (host, str(port + 1)))

		self.tts = TTS()

		# maybe change this to an env variable ... do travis.ci?
		# db = fs.FileStorage()
		# db.readYaml(YAML_FILE)
		# wit_token = db.getKey('WIT_TOKEN')

		# if wit_token is None:
		# 	self.logger.info('Need Wit.ai token, exiting now ...')
		# 	exit()
		# else:
		# 	self.logger.info('Wit.ai API token %s', wit_token)
		#
		# self.input = wi.WitInput(wit_token)

		# Grab plugins
		# self.readPlugins()

		results = """--------------------------
		Sound Server up
		Pub[results]: %s:%d
		Sub[text]: %s:%d
		Modules: %d
		--------------------------
		"""
		self.logger.info(results, host, port, host, port + 1, len(self.modules))

	def readPlugins(self, path):
		"""
		Clears the current modules and reads in all plugins located in path
		in: path to plugins
		out: none
		"""
		self.modules = []
		sys.path.insert(0, path)
		for f in os.listdir(path):
			fname, ext = os.path.splitext(f)
			if ext == '.py' and fname != 'Module' and fname != '__init__':
				print('file:', fname, ext)
				mod = __import__(fname)
				m = mod.Plugin()
				self.modules.append(m)
		sys.path.pop(0)

	"""
	Converts text to speech using tools in the OS
	in: text
	out: None
	"""
	def speak(self, txt):
		# if True:
		# 	# fname = self.tts.tts(txt)
		# 	# os.system('afplay %s'%(fname))
		# 	print('speak:', txt)
		# else:
		# 	if self.os == 'Darwin': os.system('say -v vicki ' + txt)
		# 	elif self.os == 'Linux': os.system('say ' + txt)
		# 	else: self.logger.info('speak() error')
		self.tts.say(txt)

	def search(self, txt):
		"""
		Searches through all plugins to find one that can process this intent
		in: struct{'intent': '', 'entities': ''}
		out: text (answer from plugin or '' if nothing could handle it)
		"""
		for m in self.modules:
			if m.test(txt):
				# print result
				ans = m.process()
				self.logger.debug('found plugin response: ' + ans)
				return ans
		return ''

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

				txt = self.search(result)

				if txt == 'exit_loop':
					loop = False
				elif txt == 'empty' or not txt:
					self.logger.info('no plugin response')
					continue
				else:
					self.logger.debug('response' + txt)
					self.speak(txt)

			self.speak('Good bye ...')

		except KeyboardInterrupt:
			print('{} exiting'.format(__name__))
			raise KeyboardInterrupt


if __name__ == '__main__':
	# s = SoundServer('/Users/kevin/Dropbox/accounts.yaml')
	# token = os.getenv('WIT')
	s = SoundServer()
	s.readPlugins()  # what should I do for this??
	s.start()
	print('bye ...')



import speech_recognition as sr

def loop(r):
	audio = None
	ret = ''

	with sr.Microphone() as source:
		# r.adjust_for_ambient_noise(source)
		print("Say something!")
		# audio = None
		audio = r.listen(source, 1.0)

	ret = r.recognize_sphinx(audio)

	print(">>" + ret)

	if ret == 'quit':
		exit()

def main2():
	# obtain audio from the microphone
	r = sr.Recognizer()

	while True:
		with sr.Microphone() as source:
			r.adjust_for_ambient_noise(source)

		try:
			loop(r)

		except sr.WaitTimeoutError as e:
			pass

		except KeyboardInterrupt as e:
			print('Ctrl-c ... bye')
			break
