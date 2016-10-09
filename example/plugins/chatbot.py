#!/usr/bin/env python

import random
from pygecko.lib.Chatbot import Base
from pygecko.lib.Chatbot import Chatbot
from pygecko.lib.TTS import TTS
import time


class Command(Base):
	"""
	Expect commands like:
		robot go forward|backwards|left|right
		robot stop|halt
		robot turn around|left|right
	"""
	def __init__(self, robot_name='robot'):
		self.patterns = [
			r'(.*) go (.*)',
			r'(.*) (stop|halt)',
			r'(.*) turn (around|left|right)'
		]
		self.name = robot_name

	def test(self, txt):
		self.line = None
		ret = self.analyze(txt)
		if ret:
			# print(ret.group())
			if ret.group(1) == self.name:
				self.line = ret  # save for later
				# self.cmd = {'cmd': 'go', 'dir', ret.group(2)}
				return True
		return False

	def process(self):
		return '{0} command - {1}'.format(self.line.group(1), self.line.group(2))


class StarWars(Base):
	def __init__(self):
		self.patterns = [
			r'(.*) star wars (.*)',
			r'(.*) star wars'
		]

	def test(self, txt):
		ret = self.analyze(txt)
		if ret:
			return True
		else:
			return False

	def process(self):
		return 'I like star wars too!'


class TimeDate(Base):
	def __init__(self):
		self.patterns = [
			r'what (time|date) is it',
			r'what is the (time|date)',
			r'what is (today|tomorrow) date'
		]

	def date(self, offset=0):
		t = time.localtime()
		day = t[2]+offset  # this won't work perfectly
		months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
		mon = months[t[1] - 1]
		yr = t[0]
		resp = 'The date is {0:d} {1!s} {2:d}'.format(day, mon, yr)
		return resp

	def time(self):
		t = time.localtime()
		hrs = t[3]
		if hrs > 12:
			hrs = hrs - 12
			ampm = 'pm'
		else:
			ampm = 'am'
		mins = t[4]
		resp = 'The current time is {0:d} {1:d} {2!s}'.format(hrs, mins, ampm)
		return resp

	def test(self, txt):
		ret = self.analyze(txt)
		if ret:
			self.key = ret.group(1)
			return True
		else:
			return False

	def process(self):
		if self.key == 'time':
			return self.time()
		elif self.key == 'date':
			return self.date()
		elif self.key == 'today':
			return self.date()
		elif self.key == 'tomorrow':
			return self.date()
		else:
			return ''


class Greeting(Base):
	def __init__(self, robot_name='robot'):
		self.patterns = [
			r'(.*) (hello|hi|greetings|ola|good day)'
			# r'(hello|hi|greetings|ola|good day)'
		]
		self.name = robot_name

	def test(self, txt):
		ret = self.analyze(txt)
		if ret and ret.group(1) == self.name:
			return True
		else:
			return False

	def process(self):
		response = [
			'hi',
			'hello yourself',
			'hey',
			'ola',
			'guten tag',
			'right back at you'
		]
		return random.choice(response)


class Exit(Base):
	def __init__(self):
		self.patterns = [
			r'(.*)  (quit|exit|shutdown)',
			r'(quit|exit|shutdown|bye)'
		]

	def test(self, txt):
		# print('exit', txt)
		ret = self.analyze(txt)
		if ret:
			return True
		else:
			return False

	def process(self):
		print('ok ... bye')
		exit()


def main():
	tts = TTS()
	tts.setOptions('-v Karen')  # this works on macOS and say
	cb = Chatbot()
	name = 'bob'
	plugins = [StarWars(), Command(name), Exit(), Greeting(name), TimeDate()]
	cb.setPlugins(plugins)
	while True:
		txt = raw_input('>> ')
		ans = cb.run(txt)
		if ans:
			print ans
			tts.say(ans)

if __name__ == "__main__":
	main()
