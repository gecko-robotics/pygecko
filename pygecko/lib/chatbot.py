#!/usr/bin/env python

from __future__ import print_function
import re
# import sys
# import os


class Base(object):
	"""
	Base class for plugin modules for the chatbot
	"""
	def analyze(self, txt):
		for pattern in self.patterns:
			match = re.search(pattern, txt.rstrip(".!?"), re.I)  # re.I is case insensative
			if match:
				return match
		return False


class Chatbot(object):
	def __init__(self):
		self.plugins = []

	# def readPlugins(self, path):
	# 	"""
	# 	Clears the current modules and reads in all plugins located in path
	# 	in: path to plugins
	# 	out: none
	# 	"""
	# 	self.plugins = []
	# 	sys.path.insert(0, path)
	# 	for f in os.listdir(path):
	# 		fname, ext = os.path.splitext(f)
	# 		if ext == '.py' and fname != 'Module' and fname != '__init__':
	# 			print('file:', fname, ext)
	# 			mod = __import__(fname)
	# 			m = mod.Plugin()
	# 			self.plugins.append(m)
	# 	sys.path.pop(0)

	def setPlugins(self, plugins):
		self.plugins = plugins

	def appendPlugins(self, plugins):
		self.plugins.append(plugins)

	def run(self, txt):
		try:
			for p in self.plugins:
				if p.test(txt):
					ans = p.process()
					return ans
			# return ''
		except:
			# print('Oops ... chatbot')
			raise


def main():
	print('I am a mad man with a little blue box')

if __name__ == "__main__":
	main()
