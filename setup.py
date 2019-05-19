from __future__ import print_function
from setuptools import setup
from build_utils import BuildCommand
from build_utils import PublishCommand
from build_utils import BinaryDistribution
from build_utils import SetGitTag
from build_utils import get_pkg_version


# ver = {}
# with open("pygecko/version.py") as fp:
#     exec(fp.read(), ver)
# VERSION = ver['__version__']

VERSION = get_pkg_version('pygecko/__init__.py')

PACKAGE_NAME = 'pygecko'
BuildCommand.pkg = PACKAGE_NAME
BuildCommand.py2 = False  # not supporting python2 anymore
# BuildCommand.test = False  # don't do tests
PublishCommand.pkg = PACKAGE_NAME
PublishCommand.version = VERSION
SetGitTag.version = VERSION
README = open('readme.md').read()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author="Kevin Walchko",
    keywords=['framework', 'robotic', 'robot', 'vision', 'ros', 'distributed'],
    author_email="walchko@noreply.github.com",
    description="A python robotic framework and tools",
    license="MIT",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
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
        'pyyaml',         # config files
        'psutil',
        'simplejson',     # config files
        'msgpack',        # efficient message serialization through zmq
        'pyzmq',          # connecting to different processes and computers
        # 'bjoern',         # http server, multiple connections
        # 'the_collector',  # saving data
        'colorama',       # log messages
        'numpy',          # basic image stuff ... remove/optional?
        'build_utils'     # installing and building the library
    ],
    url="https://github.com/MomsFriendlyRobotCompany/{}".format(PACKAGE_NAME),
    long_description=README,
    long_description_content_type='text/markdown',
    packages=[PACKAGE_NAME],
    cmdclass={
        'publish': PublishCommand,
        'make': BuildCommand,
        'tag': SetGitTag
    },
    scripts=[
        'bin/geckocore.py',
        'bin/pycore.py',
        'bin/geckolaunch.py',
        # 'bin/mjpeg_server.py',  # why? use opencvutils instead
        # 'bin/bag_play.py',
        # 'bin/bag_record.py',
        # 'bin/camera_calibrate.py',
        # 'bin/image_view.py',
        # 'bin/service.py',  # fix
        'bin/gecko_log_display.py',
        'bin/geckotopic.py',
        'bin/twist_keyboard.py'
        # 'bin/video.py',
        # 'bin/webserver.py'
    ]
)
