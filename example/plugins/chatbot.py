#!/usr/bin/env python

import re
import random


class Base(object):
	def analyze(self, txt):
		for pattern in self.patterns:
			match = re.search(pattern, txt.rstrip(".!?"), re.I)  # re.I is case insensative
			if match:
				return match
		return False


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
		return 'star wars - good'


class Greeting(Base):
	def __init__(self, robot_name='robot'):
		self.patterns = [
			r'(.*) (hello|hi|greetings|ola|good day)'
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
	while True:
		statement = raw_input(">> ")
		name = 'bob'

		# print analyze2(statement)
		plugins = [StarWars(), Command(name), Exit(), Greeting(name)]
		for p in plugins:
			if p.test(statement):
				print p.process()
				break

		# if statement == 'quit':
		# 	return

if __name__ == "__main__":
	main()
