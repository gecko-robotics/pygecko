import os
from setuptools import setup
from pygecko import __version__ as VERSION
from setuptools.command.test import test as TestCommand


class NoseTestCommand(TestCommand):
	def run_tests(self):
		print('Running nose tests ...')
		os.system('nosetests -v test/test.py')


class PublishCommand(TestCommand):
	def run_tests(self):
		print('Publishing to PyPi ...')
		os.system("python setup.py sdist")
		os.system("twine upload dist/pygecko-{}.tar.gz".format(VERSION))


class GitTagCommand(TestCommand):
	def run_tests(self):
		print('Creating a tag for version {} on git ...'.format(VERSION))
		os.system("git tag -a {} -m 'version {}'".format(VERSION, VERSION))
		os.system("git push --tags")


class CleanCommand(TestCommand):
	def run_tests(self):
		print('Cleanning up ...')
		os.system('rm -fr pygecko.egg-info dist')

readme = open('README.rst').read()

setup(
	name="pygecko",
	version=VERSION,
	author="Kevin Walchko",
	keywords=['framework', 'robotic', 'robot', 'vision', 'ros', 'distributed'],
	author_email="kevin.walchko@outlook.com",
	description="A python robotic framework and tools",
	license="MIT",
	classifiers=[
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 2 :: Only',
		'Operating System :: Unix',
		'Operating System :: POSIX :: Linux',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: POSIX',
		'Topic :: Scientific/Engineering',
		'Topic :: Scientific/Engineering :: Artificial Intelligence',
		'Topic :: Scientific/Engineering :: Image Recognition',
		'Topic :: Software Development :: Libraries :: Python Modules',
	],
	install_requires=['pyrk', 'pyyaml', 'pyzmq', 'simplejson', 'pyserial', 'numpy', 'nose', 'pyaudio'],
	url="https://github.com/walchko/pygecko",
	long_description=readme,
	packages=["pygecko"],
	# scripts=[
	# 	'chi/tools/mjpeg-server.py'
	# ]
	# entry_points={
	# 	'console_scripts': [
	# 		# 'pyarchey=pyarchey.pyarchey:main',
	# 	],
	# },
)
