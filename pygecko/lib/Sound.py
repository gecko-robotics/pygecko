#!/usr/bin/env python

import os
from wit import Wit
import ZmqClass as zmq
from time import sleep


class Audio(object):
	# path ?

	def play(self, snd):
		os.system('afplay {0!s}'.format((snd)))

	def save(self, filename, text):
		"""
		Convert text to speech and then save the output as a wav file. This is
		primarily useful for testing/debuging.

		You must install ``say``

		kevin@Logan ~ $ file test.wav
		test.wav: RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 16000 Hz
		"""
		os.system('say -o {} --data-format LEI16@16000 {}'.format(filename, text))


class pyWit(object):
	def __init__(self, token_env='WIT'):
		token = os.environ[token_env]
		self.client = Wit(token)
		self.speech_headers = {
			'authorization': 'Bearer ' + token,
			# 'accept': 'application/vnd.wit.20160330+json'
			'Content-Type': 'audio/wav'
			# 'Content-Type': 'audio/raw;encoding=signed-integer;bits=16;rate=16000;endian=little'
		}

	@staticmethod
	def max(a):
		ret = None
		if not a:
			pass
		elif len(a) == 1:
			ret = a[0]
		else:
			ret = a.pop(0)
			for r in a:
				if r['confidence'] > ret['confidence']:
					ret = r

		return ret

	def filter_return(self, ans):
		pass

	def message(self, msg):
		intent = None
		confidence = 0.0
		ans = self.client.message(msg)
		# pprint(ans)

		if ans:
			ans = self.max(ans['outcomes'])
			intent = ans['intent']
			confidence = ans['confidence']
			# print('Result {} at {:.2f}%'.format(intent, confidence*100.0))
		return (intent, confidence, ans['entities'])

	def speech(self, wav):
		intent = None
		confidence = 0.0
		ans = self.client.speech(wav, headers=self.speech_headers)
		if ans:
			ans = self.max(ans['outcomes'])
			# print(ans)
			intent = ans['intent']
			confidence = ans['confidence']
			# print('Result {} at {:.2f}%'.format(intent, confidence*100.0))
		return (intent, confidence, ans['entities'])

	def run(self, topics, port, actions, confidence_level=0.6):
		sub = zmq.Sub(topics=topics, connect_to=('localhost', port))
		print('[>] {} subscribed to {} on {}:{}'.format('pywitServer', topics, 'localhost', port))

		while True:
			topic, msg = sub.recv()
			if msg:
				if 'message' in msg:
					intent, confidence, ent = self.message(msg['message'])

				elif 'wav' in msg:
					intent, confidence, ent = self.speech(msg['wav'])

				if intent and (confidence >= confidence_level):
					if intent in actions:
						func = actions[intent]
						func()
			sleep(2)
			# print('\n------------------------')
