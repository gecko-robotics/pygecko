#!/usr/bin/env python

from __future__ import print_function
from pygecko.lib import pyWit
from pygecko.lib import Audio
import os
# from pprint import pprint

# nosetests -v -s test_wit.py
# -s prints to std out
# -v is vervose

# travis.ci
# install gnustep to get say


# these are a list of messages and the proper answer (intent)
tests = [
	# message, intent
	['hello', 'greeting'],
	['so how do you feel?', 'feelings'],
	['can you play venture brothers', 'tv_movie_sounds'],
	['I like star wars', 'tv_movie_sounds'],
	['tell me a joke', 'joke'],
	['do you know the time', 'time'],
	['what is the weather on Friday', 'weather'],
]


def test_message():
	pw = pyWit()
	print(' ')  # make pretty

	for text, intent in tests:
		ret, conf, ent = pw.message(text)
		print(' > Test {}[{:.2f}] with "{}"'.format(intent, conf*100, text))
		# pprint(ent)
		assert intent == ret


def test_speech():
	a = Audio()
	pw = pyWit()
	print(' ')  # make pretty

	filename = 'temp.wav'
	for text, intent in tests:
		a.save(filename, text)  # create an audio file
		wav = open(filename, 'rb')  # only give it a file handler

		ret, conf, ent = pw.speech(wav)
		print(' > Test {}[{:.2f}] with "{}"'.format(intent, conf*100, text))
		os.remove(filename)
		assert ret == intent


def test_max():
	"""
	Find the maximum confidence in the array.
	"""
	test = [
		{'confidence': 0.30, 'intent': 'wrong'},
		{'confidence': 0.90, 'intent': 'right'},
		{'confidence': 0.50, 'intent': 'wrong'},
		{'confidence': 0.80, 'intent': 'wrong'},
		{'confidence': 0.10, 'intent': 'wrong'}
	]

	ans = pyWit.max(test)
	assert ans['intent'] == 'right'
