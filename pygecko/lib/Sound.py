#!/usr/bin/env python

import os
import wave


def playSound(snd):
	os.system('afplay {0!s}'.format((snd)))


class WaveSound(object):
	def saveWaveFile(self, filename):
		"""
		Save file to disk
		"""
		pass

	def readWaveFile(self, filename):
		"""
		Read wave file into memory from disk/StringIO
		"""
		pass

	def playWave(self, wave):
		"""
		Play file in memory
		"""
		pass

	def playWaveFile(self, filename):
		"""
		Play file on disk
		"""
		pass
