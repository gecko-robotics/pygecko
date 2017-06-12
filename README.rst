
.. image:: https://github.com/MomsFriendlyRobotCompany/pygecko/raw/master/pics/gecko.jpg
	:target: https://github.com/MomsFriendlyRobotCompany/pygecko

pyGecko
============================

.. image:: https://img.shields.io/pypi/v/pygecko.svg
	:target: https://github.com/MomsFriendlyRobotCompany/pygecko
.. image:: https://img.shields.io/pypi/l/pygecko.svg
	:target: https://github.com/MomsFriendlyRobotCompany/pygecko
.. image:: https://travis-ci.org/MomsFriendlyRobotCompany/pygecko.svg?branch=master
	:target: https://travis-ci.org/MomsFriendlyRobotCompany/pygecko
.. image:: https://landscape.io/github/MomsFriendlyRobotCompany/pygecko/master/landscape.svg?style=flat
	:target: https://landscape.io/github/MomsFriendlyRobotCompany/pygecko/master
	:alt: Code Health
.. image:: https://requires.io/github/MomsFriendlyRobotCompany/pygecko/requirements.svg?branch=master
	:target: https://requires.io/github/MomsFriendlyRobotCompany/pygecko/requirements/?branch=master
	:alt: Requirements Status

My robot software.

* Doesn't use `ROS <http://ros.org>`_, ROS is a pain to install and maintain on macOS and various linux systems
	* Uses some of the same ideas, but not RPC-XML
* Uses `Zero MQ <http://http://zeromq.org/>`_ instead of ``roscore``
* Uses OpenCV to process on-board or stream video off-board to remote
* All of this runs on `Raspberry Pi3 <http://www.raspberrypi.org>`_

Documentation
-------------------

**Note:** This re-write is still very early and not fully running yet, just
parts.

The documentation can be found `here <docs/Markdown>`_.

Install
-----------

Use ``brew`` or ``apt-get`` to install these dependencies:

* zeromq
* opencv 3.x

pip
~~~~~

The recommended way to install this library is::

	pip install pygecko

Development
~~~~~~~~~~~~~

If you wish to develop and submit git-pulls, you can do::

	git clone https://github.com/MomsFriendlyRobotCompany/pygecko
	cd pygecko
	pip install -e .

Testing
~~~~~~~~~

Since I have both python2 and python3 installed, I need to test with both::

	python2 -m nose *.py
	python3 -m nose *.py

**Warning:** python3 is not fully supported yet, it is giving me problems. Only
python2 is currently supported.

Layout
------------

pyGecko **still in development**

* example/servers: main message server nodes

	* Speech server
	* Navigation server
	* Vision processing server
	* VideoOdometry server

* bin: command line programs

	* topic reader/creator
	* bag play/record
	* image viewer
	* mjpeg streamer
	* keyboard controller

* pygecko: mostly classes

	* bag
	* camera calibrator
	* chatbot
	* file storage
	* messages
	* pywit
	* audio
	* zmq

Tools
---------

This directory contains several tools for the robot:

==================== ======= ================
Executable           Stable  Description
==================== ======= ================
camera_calibrate.py  Y       performs camera calibration using either a chessboard or asymmetric circle target. Target patterns are in the `patterns` folder.
topic.py             N       send various commands to the robot [work in progress]
image_view           Y       subscribe to image messages and display them for debugging
mjpeg-server         Y       create a web server which serves up an mjpeg stream from a camera. Any web browser on any device can see this stream (easier than image_view)
video.py             Y       capture images or a video clip from a camera
webserver.py         N       serve up a web page containing debugging and status info for the robot
bag_play/record      Y       saves messages to a file so they can be replayed off-line later
twist_keyboard       Y       simple keyboard interface to send twist messages to a robot
==================== ======= ================

**Note:** Please take stable with a grain of salt ... all of this is still in major development.

**Note:** There is some duplication between these, and it will eventually be sorted out.


ToDo
-----

* fix speech ... not sure best way to do this
* better modularity for various robots ... not sure how to do this
	* multiple robots use same/similar software ... not sure how to best divide things up
* ``mjpeg_server``
	* only handles one connection at a time ... make threaded?
	* sometimes the video stream is slow to load, but then it works fine
	* handle client disconnect (broken pipe - 32) better
* ``quaternions`` - use/update
* implement a simple dynamic html server that takes json data in and produces webpages of diagnostic/status info

History
-----------

``pyGecko`` comes from my previous robotics projects that I have been working
on for years. Why gecko?? I am from Florida and I remember seeing a lot of geckos
running around when I was at college ... my cats were scared of them.

Change Log
-------------

============ ======= ============================
2017-May-14  0.8.3   updates and refactor
2017-Apr-02  0.8.2   fix pypi doc and refactor
2017-Mar-19  0.7.0   refactored
2017-Mar-12  0.6.0   changed messages from dict to classes
2016-Dec-26  0.5.0   refactor
2016-Oct-09  0.4.1   published to PyPi
2010-Mar-10  0.0.1   init
============ ======= ============================


MIT License
---------------

**Copyright (c) 2010 Kevin J. Walchko**

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
