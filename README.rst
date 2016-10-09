pyGecko
============================

.. image:: https://github.com/walchko/pygecko/raw/master/pics/noun_11784_cc.png
	:align: center
	:width: 200 px

My robot software.

* Doesn't use `ROS <http://ros.org>`_, ROS is a pain to install and maintain on OSX and various linux systems
	* Uses some of the same ideas, but not RPC-XML
* Uses `Zero MQ <http://http://zeromq.org/>`_ instead of ``roscore``
* Uses OpenCV to process on-board or stream video off-board to remote
* All of this runs on `Raspberry Pi3 <http://www.raspberrypi.org>`_

**Note:** This re-write is still very early and not fully running yet, just parts.

Install
-----------

Use ``brew`` or ``apt-get`` to install:

* zeromq
* opencv 3.x
* cmu pocket sphinx (the most recent version, you will probably have to build it)
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

* servers: main nodes

	* Speech server
	* Navigation server
	* Vision processing server
	* VideoOdometry server
	
* tools: command line programs

	* Topic reader/creator
	* bag play/record
	* image viewer
	* mjpeg streamer
	* keyboard
	
* lib: mostly classes

	* bag
	* camera calibrator
	* chatbot
	* file storage
	* messages
	* microphone
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


History
-----------

pyGecko comes from my previous robotics projects that I have been working
on for years.

Change Log
-------------

========== ======= =============================
2016-10-09 0.4.1   published to PyPi
2010-03-10 0.0.1   init
========== ======= =============================

