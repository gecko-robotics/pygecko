from __future__ import print_function
from setuptools import setup
from pygecko.version import __version__ as VERSION
from build_utils import BuildCommand
from build_utils import PublishCommand
from build_utils import BinaryDistribution


PACKAGE_NAME = 'pygecko'
BuildCommand.pkg = PACKAGE_NAME
BuildCommand.py3 = False  # python 3 build isn't working yet with zmq, need time to fix
PublishCommand.pkg = PACKAGE_NAME
PublishCommand.version = VERSION
README = open('README.rst').read()

setup(
	name=PACKAGE_NAME,
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
		# 'Programming Language :: Python :: 3.6',
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
		# 'pyrk',
		# 'numdifftools',  # do I really need this? pulls in scipy (issues with RPi), move to drivers?
		'pyyaml',
		'pyzmq',
		'zmq',
		'simplejson',
		'pyserial',
		'numpy',
		'opencvutils',
		# 'wit',  # do I really need this? Voice should be an add on?
		# 'pyaudio',  # this is crap!
		'quaternions',
		'build_utils'
	],
	url="https://github.com/walchko/{}".format(PACKAGE_NAME),
	long_description=README,
	packages=['pygecko'],
	cmdclass={
		'publish': PublishCommand,
		'make': BuildCommand
	},
	scripts=[
		'bin/mjpeg_server.py',  # why? use opencvutils instead
		'bin/bag_play.py',
		'bin/bag_record.py',
		'bin/camera_calibrate.py',
		'bin/image_view.py',
		'bin/service.py',  # fix
		'bin/topic_echo.py',
		'bin/topic_pub.py',
		'bin/twist_keyboard.py'
		# 'bin/video.py',
		# 'bin/webserver.py'
	]
)
