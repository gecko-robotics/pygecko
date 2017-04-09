import os
from setuptools import setup
from pygecko import __version__ as VERSION
from setuptools.command.test import test as TestCommand
from setuptools.dist import Distribution


class BinaryDistribution(Distribution):
	def is_pure(self):
		return False


class BuildCommand(TestCommand):
	"""Build binaries/packages"""
	def run_tests(self):
		print('Delete dist directory and clean up binary files')
		os.system('rm -fr dist')
		os.system('rm pygecko/*.pyc')
		os.system('rm pygecko/__pycache__/*.pyc')
		print('Run Nose tests')
		ret = os.system("cd tests && python2 -m nose -v *.py")
		if ret > 0:
			print('<<< Python2 nose tests failed >>>')
			return
		# ret = os.system("cd tests && python3 -m nose -v *.py")
		if ret > 0:
			print('<<< Python3 nose tests failed >>>')
			return

		print('Building packages ...')
		os.system("python setup.py sdist")
		os.system("python2 setup.py bdist_wheel")
		# os.system("python3 setup.py bdist_wheel")


class PublishCommand(TestCommand):
	"""Publish to Pypi"""
	def run_tests(self):
		print('Publishing to PyPi ...')
		os.system("twine upload dist/fake_rpi-{}*".format(VERSION))


README = open('README.rst').read()

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
		'Programming Language :: Python :: 3.6',
		'Operating System :: Unix',
		'Operating System :: POSIX :: Linux',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: POSIX',
		'Topic :: Scientific/Engineering',
		'Topic :: Scientific/Engineering :: Artificial Intelligence',
		'Topic :: Scientific/Engineering :: Image Recognition',
		'Topic :: Software Development :: Libraries :: Python Modules'
	],
	install_requires=[
		'pyrk',
		'numdifftools',
		'pyyaml',
		'pyzmq',
		'zmq',
		'simplejson',
		'pyserial',
		'numpy',
		'opencvutils',
		'wit',
		# 'pyaudio',  # this is crap!
		'quaternions'
	],
	url="https://github.com/walchko/pygecko",
	long_description=README,
	packages=['pygecko'],
	cmdclass={
		'publish': PublishCommand,
		'make': BuildCommand
	},
	scripts=[
		'bin/mjpeg_server.py',
		'bin/bag_play.py',
		'bin/bag_record.py',
		'bin/camera_calibrate.py',
		'bin/image_view.py',
		'bin/service.py',
		'bin/topic_echo.py',
		'bin/topic_pub.py',
		'bin/twist_keyboard.py'
		# 'bin/video.py',
		# 'bin/webserver.py'
	]
)
