# :lizard:  pyGecko

ok, so I am redoing this whole thing! I have learned a lot and I don't like
how I was doing it before.

Changes:

- use more built in python libraries
- take advantage of multiprocessing more: events, namespaces, etc
- use Google's protobuf as a serializer instead of rolling my own with json/dicts
- less of a library to maintain and more of a "How to code"


Architecture:

- everything has to be lightweight enough to run on a raspberry pi
    - might code in some C stuff for speed if necessary, but I don't think I need it
- used `Process` to get work done and write them in their own file
    - maybe write a simple wrapper to reduce coding
- main program spins up processes for execution on local machine
    - use `Event` to shut things down
    - have simple webserver to display plots and camera feed
        - having hard time finding small/fast/simple async python solution to
        stream video/data to multiple users
        - node.js works nice, but then need python -> node bridge (socket.io?)
