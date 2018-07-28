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
