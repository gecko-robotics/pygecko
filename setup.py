from __future__ import print_function
from setuptools import setup
from pygecko import __version__ as VERSION
from build_utils import BuildCommand
from build_utils import PublishCommand
from build_utils import BinaryDistribution


BuildCommand.pkg = 'pygecko'
BuildCommand.py3 = False
PublishCommand.pkg = 'pygecko'
PublishCommand.version = VERSION
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
		'quaternions',
		'build_utils'
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
