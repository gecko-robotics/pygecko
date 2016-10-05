pyGecko
============================

.. image:: noun_11784_cc.png
	:align: center

My robot software.

* Doesn't use `ROS <http://ros.org>`_, ROS is a pain to install and maintain on OSX and various linux systems
	* Uses some of the same ideas, but not RPC-XML
* Uses `Zero MQ <http://http://zeromq.org/>`_ instead of ``roscore``
* Uses my PS4 controller with PySDL2
* Uses OpenCV to process on-board or stream video off-board to remote
* All of this runs on `Raspberry Pi3 <http://www.raspberrypi.org>`_

**Note:** This re-write is still very early and not fully running yet, just parts.

Install
-----------

Use ``brew`` or ``apt-get`` to install:

* zeromq
* opencv 3.x
* cmu pocket sphinx (the most recent version)
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

* Audio server
* Navigation server
* Vision processing server
* Keyboard node
* Tools - command line programs
	* Topic reader/creator
	* bag play/record
	* image viewer
	* mjpeg streamer
* lib - mostly classes
	* bag
	* camera calibrator
	* chatbot
	* file storage
	* messages
	* sox
	* zmq

# Tools

This directory contains several tools for the robot:

| Executable         | Stable  | Description |
|--------------------|---------|-------------|
| camera_calibrate.py | Y | performs camera calibration using either a chessboard or asymmetric circle target. Target patterns are in the `patterns` folder. |
| topic.py     | N | send various commands to the robot [work in progress] |
| image_view   | Y | subscribe to image messages and display them for debugging |
| mjpeg-server | Y | create a web server which serves up an mjpeg stream from a camera. Any web browser on any device can see this stream (easier than image_view) |
| video.py     | Y | capture images or a video clip from a camera |
| wevserver.py | N | serve up a web page containing debugging and status info for the robot |

**Note:** Please take stable with a grain of salt ... all of this is still in major development.

**Note:** There is some duplication between these, and it will eventually be sorted out.


History
-----------

pyGecko comes from my previous robotics projects that I have been working
on for years.

Change Log
-------------

========== ======= =============================
2016-10-05 0.3.0   published to PyPi
2010-03-10 0.0.1   init
========== ======= =============================

Misc
-----

- Gecko image by John Melven from the `Noun Project <https://thenounproject.com/search/?q=gecko&i=11784>`_
