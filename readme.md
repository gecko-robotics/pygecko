# :lizard:  pyGecko

ok, so I am redoing this whole thing! I have learned a lot and I don't like
how I was doing it before.

## My robot software.

- Doesn't use [ROS](http://ros.org), ROS is a pain to install and maintain
on macOS and various linux systems
    - Uses some of the same ideas, constructs, architecture ideas, APIs but
    not strictly adhering to them
- Uses [Zero MQ](http://http://zeromq.org/) as the process to process communication
(uses both TCP and UDS) instead of RPC-XML
    - looked at Google's protobuf, but was more complex than I needed
    - using [`msgpack`](https://msgpack.org/index.html) to serialize data
    - instead of `roscore` use `geckocore.py`
    - instead of `roslaunch` use `geckolaunch.py`
- Uses [`the_collector`]((https://github.com/MomsFriendlyRobotCompany/the_collector))
to save/retrieve data to a file
- `simplejson`/`pyyaml` - config and launch files
- All of this runs on `Raspberry Pi3 <http://www.raspberrypi.org>`_

# Architecture

TBD

# Todo

These are ideas I really have not flushed out yet

- serial-to-tcp to collect data
- python/c example to use unix domain sockets
- webserver displaying info
    - `bjoern` - efficient web server written in C with python bindings
- data logger over tcp/unix domain sockets
    - need to have simple setup class to make this easy
    - automatically append time-date
    - put every collect into a folder
    - webpage serve up data
        - show meta data for collect
        - allow deletion of folder/data
        - show available and used hard drive space

# Change Log

Date        |Version| Notes
------------|-------|---------------------------------
2018-Jul-28 | 1.0.0 | totally nuked everything from orbit and started over
2017-May-14 | 0.8.3 | updates and refactor
2017-Apr-02 | 0.8.2 | fix pypi doc and refactor
2017-Mar-19 | 0.7.0 | refactored
2017-Mar-12 | 0.6.0 | changed messages from dict to classes
2016-Dec-26 | 0.5.0 | refactor
2016-Oct-09 | 0.4.1 | published to PyPi
2010-Mar-10 | 0.0.1 | init


# MIT License

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
