pyGecko
============================

.. image:: https://github.com/walchko/pygecko/raw/master/pics/gecko.jpg
	:align: center
	:width: 200 px


.. image:: https://img.shields.io/pypi/v/pygecko.svg
	:target: https://github.com/walchko/pygecko
.. image:: https://img.shields.io/pypi/l/pygecko.svg
	:target: https://github.com/walchko/pygecko
.. image:: https://travis-ci.org/walchko/pygecko.svg?branch=master
	:target: https://travis-ci.org/walchko/pygecko
.. image:: https://api.codacy.com/project/badge/Grade/7e526b9907754837a15beff59d393e10
	:target: https://www.codacy.com/app/kevin-walchko/pygecko?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=walchko/pygecko&amp;utm_campaign=Badge_Grade
.. image:: https://requires.io/github/walchko/pygecko/requirements.svg?branch=master
	:target: https://requires.io/github/walchko/pygecko/requirements/?branch=master
	:alt: Requirements Status

My robot software.

* Doesn't use `ROS <http://ros.org>`_, ROS is a pain to install and maintain on
OSX and various linux systems
	* Uses some of the same ideas, but not RPC-XML
* Uses `Zero MQ <http://http://zeromq.org/>`_ instead of ``roscore``
* Uses OpenCV to process on-board or stream video off-board to remote
* All of this runs on `Raspberry Pi3 <http://www.raspberrypi.org>`_

**Note:** This re-write is still very early and not fully running yet, just
parts.

Install
-----------

Use ``brew`` or ``apt-get`` to install:

* zeromq
* opencv 3.x
* [optional] SDL 2.0 for PS4 joystick control

pip
~~~~~

::

	pip install pygecko

Development
~~~~~~~~~~~~~

::

	git clone https://github.com/walchko/pygecko
	cd pygecko
	pip install -e .


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
* ``opencvutils`` - replacing ``lib/Camera.py`` and move calibration stuff to it
	* these are good capabilities that can be used beyond just this library, make a stand alone library/tool
* ``simplehtml`` - use for dynamic webpages
* ``quaternions`` - use/update
* implement a simple dynamic html server that takes json data in and produces webpages of diagnostic/status info

History
-----------

``pyGecko`` comes from my previous robotics projects that I have been working
on for years.

Change Log
-------------

============ ======= ============================
2017-Mar-19  0.7.0   this is now a library in ``pygecko``, ``tools`` moved to ``bin``, and ``servers`` were put under examples because you will always have to tweak the server for your application
2017-Mar-12  0.6.0   changed messages from dict to classes
2016-Dec-26  0.5.0   refactor
2016-Oct-09  0.4.1   published to PyPi
2010-Mar-10  0.0.1   init
============ ======= =============================

License
---------

**The MIT License (MIT)**

Copyright (c) 2010 Kevin J. Walchko

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
