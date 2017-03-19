#!/usr/bin/env python

from __future__ import print_function
from subprocess import call


class TTS(object):
	"""
	"""
	def __init__(self, tts=None):
		"""
		You can pass in a specific tts program or let it search for one to
		use. It searches for: say, espeak, spd-say. If no program is found, it uses
		echo to print text to the command line

		"""
		found = False
		if not tts:
			for cmd in ['espeak', 'spd-say', 'say']:
				if call(['which -s {}'.format(cmd)], shell=True) == 0:
					self.tts = [cmd]
					# self.tts = cmd
					found = True
					break
			if not found:
				print('could not find a tts program, using echo instead')
				self.tts = 'echo'
		else:
			self.tts = tts

	def setOptions(self, options):
		"""
		Change the default options
		"""
		self.tts.append(options)

	def say(self, txt):
		"""
		Speak the text passed to this function. If no tts was found, then this
		will print the text instead.
		"""
		c = self.tts[:]  # make a copy
		c.append(txt)
		call(' '.join(c), shell=True)
