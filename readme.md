# :lizard:  pyGecko

ok, so I am redoing this whole thing! I have learned a lot and I don't like
how I was doing it before.

## Issues

- zmq had too much latency ... I captured data too fast and it created a backlog
- I developed a complex, python only serialization capability that is cool, but limiting (python only)

# Changes

- use more built in python libraries
- take advantage of multiprocessing more: events, namespaces, etc
- use Google's protobuf as a serializer instead of rolling my own with json/dicts
- less of a library to maintain and more of a "How to code"


# Architecture

- all data is immutable, should be faster, smaller and eleminate the posibility
  of a user trying to change data accidentally
- everything has to be lightweight enough to run on a raspberry pi
    - might code in some C stuff for speed if necessary, but I don't think I need it
- used `Process` to get work done and write them in their own file
    - Python's multithreading is not suitable for CPU-bound tasks (because of the GIL), 
      so use `multiprocessing`
    - maybe write a simple wrapper to reduce coding
- main program spins up processes for execution on local machine
    - use `Event` to shut things down
    - have simple webserver to display plots and camera feed
        - having hard time finding small/fast/simple async python solution to
        stream video/data to multiple users
        - node.js works nice, but then need python -> node bridge (socket.io?)

# Todo

- better incorperation of imagery and cv2 ... shouldn't need to install cv2 to use things
    - how to handle imagery better
- serial-to-matplotlib?
- do Google protobufs bring anything? replace my serialization library and messaging format
    - cross platform and cross language
    - all of the hard work is done for me
- serial-to-tcp to collect data
- python/c example to use unix domain sockets
- data logger over tcp/unix domain sockets
    - need to have simple setup class to make this easy
    - automatically append time-date
    - put every collect into a folder
    - compress/zip/tar.gz data
    - nodejs webpage serve up data
        - show meta data for collect
        - allow deletion of folder/data
        - show available and used hard drive space

# Existing

- [the collector: saving data to files](https://github.com/MomsFriendlyRobotCompany/the_collector)
