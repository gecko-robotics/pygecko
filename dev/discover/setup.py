#!/usr/bin/python2.7
from setuptools import setup
requires = []
setup(
        name='hxsd',
        version='0.1.0',
        description="Simple Service discovering library",
        author="Ross Delinger",
        author_email="rossdylan@csh.rit.edu",
        url='https://github.com/rossdylan/Helixode-SD',
        packages=['hxsd'],
        install_requires=requires,
        entry_points="""
        [console_scripts]
        hxsd = hxsd:main
        """
    )

