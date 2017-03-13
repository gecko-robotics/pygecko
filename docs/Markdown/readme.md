# pyGecko

![gecko image](https://github.com/walchko/pygecko/raw/master/pics/noun_11784_cc.png)

## Overview

This is my long running hobby and what I want to get out of it:

* practice computer vision
* learn about SLAM
* remember how to do inertial navigation
* play with some machine learning

## Goals

Robot:

* has a simple personality
* can sense world around it
   * recognize certain people
   * nearby objects
   * floor (so it doesn't fall down stairs)
* can sense itself
   * hunger (power)
   * orientation
* can navigate from one location to another
   * determine how far it has traveled
   * builds a map of where it has been
* can interact with a person
   * listen/talk
   * lights/LCD colors mean different things

# Quick Start

This software is composed of individual programs (processes) that perform specific functions. They are tied together through a series of publish and subscribe messaging queues which use ZeroMQ (a serverless message system).

The robot software is broken up into individual processes (python scripts) and they can be run from the command line. The script `launch.py` (**needs updating**) is a script to launch all processes and get the robot going in one fell swoop.


## Interfaces

There are various processes running and these processes talk to each other
through multiple interfaces.

![singal flow](https://github.com/walchko/pygecko/raw/master/pics/Robot_Processes.png)

My system draws from messages defined by [ROS](www.ros.org). A list of the
interfaces is below:

| Header    | Format                                              |
|-----------|-----------------------------------------------------|
|Vector     | {x,y,z}                                             |
|Quaternion | {x,y,z,w}                                           |
|Twist      | {linear[vec],angular[vec]}                          |
|Wrench     | {force[vec],torque[vec]}                            |
|IMU        | {header, accel[vec],gyro[vec],comp[vec],temp}       |
|Range      | {header, fov[float], limits[float]{min,max}, range} |
|Image      | {header, image}                                     |
|Pose       | {position[point], orientation[quaternion]}          |
|PoseStamped| {header, position[point], orientation[quaternion]}  |
|Odom       | {header, frame[string], pose(position), twist(velocity)}  |
|Text       | {header, message[string]}                           |
|Path       | {header, poses[poseStamped]}                        |
|GetPlan    | {start[poseStamped], stop[poseStamped]}             |

Not all of these are implemented, but they are classes.

## Processes

The system is setup to run using multiple process. This adds flexibility and
modularity compared to a monolithic code base. An overview of the different
processes is shown below:

![processes](https://github.com/walchko/pygecko/raw/master/pics/Robot.png)

The above diagram shows the current processes done or under development. They
are connected by a messaging system:

* **P**: publisher
* **S**: subscriber
* **I**: a simple TCP/IP interface usually to the internet
* **V**: service

This architecture allows processes to be run or stopped without the entire system going down. This also adds a degree of robustness, since a process that crashes doesn't kill the entire system.

## Processes

* **Hardware** - controls motors, leds, servos, etc
* **Video** - was Camera, publishes images from USB camera, streams base64 encoded images
* **Video Odemetry** - processes images and estimates odometry
* **Audio** - handles voice interactions and sound effects
* **Joystick** - allows the user to send commands via a PS4 controller
* **Keyboard** - allows the user to send motion commands via keybord or type messages (bypassing microphone->speech->text conversion) to test audio plugins
* **Navigation** - uses optimal filtering to perform sensor fusion (imu, video, etc) and determine distance travelled
* **Control** - takes motion commands and calculates motor values
* **Map** - given desired start/stop/time, this will perform path planning

# Imagery

*move to better location*

These come from common ROS descriptions

|Topic            |  Description|
|---|---|
|image_raw        |  raw data from the camera driver, possibly Bayer encoded|
|image            |  monochrome, distorted|
|image_color      |  color, distorted|
|image_rect       |  monochrome, rectified|
|image_rect_color |  color, rectified|

# Install

## Pip Libraries Used

Use `pip` to install the following python libraries:

* PySDL2 - PS4 joystick
* PyYAML - read yaml config files
* pyzmq - interprocess communication library
* smbus-cffi - [I2C](https://pypi.python.org/pypi/smbus-cffi) support
* SpeechRecognition - interfaces easily with cmu-pocketsphinx for speech-to-text processing
* pyrk - kalman filtering
* pyserial - serial ports
* pyaudio - capture speech from microphone

## Adafruit

**TODO** Sort out this adafruit library mess ... there are so many and they are duplicates! Also, they just changed how they do their libraries and I need to catch up!

You will need the following libraries from Adafruit for:

###[GPIO](https://github.com/adafruit/Adafruit_Python_GPIO)

	sudo apt-get update
	sudo apt-get install build-essential python-pip python-dev python-smbus git
	git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
	cd Adafruit_Python_GPIO
	python setup.py install

###[LED Matrix](https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code):

	git clone https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git

Have a look at the LEDBackpack 8x8_pixel example

###[IMU](https://github.com/adafruit/Adafruit_Python_BNO055):

	git clone git@github.com:adafruit/Adafruit_Python_BNO055.git
	cd Adafruit_Python_BNO055
	python setup.py install


## Raspbian Libraries

	sudo apt-get install build-essential libi2c-dev i2c-tools python-dev libffi-dev
	sudo apt-get install libsdl2-dev
	sudo apt-get install libzmq3-dev
	sudo apt-get install gnustep-gui-runtime
	pip install cffi smbus-cffi
	pip install pysdl2
	pip install pyzmq


---

<p align="center">
	<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
		<img alt="Creative Commons License"  src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" />
	</a>
	<br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
</p>
