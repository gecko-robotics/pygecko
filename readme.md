# :lizard:  pyGecko

ok, so I am redoing this whole thing! I have learned a lot and I don't like
how I was doing it before.

## Issues

- zmq had too much latency ... I captured data too fast and it created a backlog
    - it also became a pain manually setting all of the required ip/port addresses
- I developed a complex, python only serialization capability that is cool, but limiting (python only)
- this became too big! if I only wanted one small thing, I had bring everything

# Changes

- use more built in python libraries
- take advantage of multiprocessing more: events, namespaces, etc
- use `msgpack`, it is simpler than Google's protobuf library and just as cross
platform, plus you can install it with a simple `pip install msgpack` command
- less of a library to maintain and more of a "How to code"
  - pygecko should be small, but import other libraries ... it is just the glue
  that holds things together

```python
import numpy as np

# Create a dummy matrix
img = np.ones((50, 50, 3), dtype=np.uint8) * 255
# Save the shape of original matrix.
img_shape = img.shape

message_image = np.ndarray.tobytes(img)

re_img = np.frombuffer(message_image, dtype=np.uint8)

# Convert back the data to original image shape.
re_img = np.reshape(re_img, img_shape)
```

# Architecture

## Libraries

- msgpack - compact efficient binary packaging of python data
- the_collector - save timestamped data
- pyzmq - IPC or machine-to-machine publish/subscribe
- simplejson/pyyaml - config files
- bjoern - efficient web server written in C with python bindings

## Ideas

- all data is immutable, should be faster, smaller and eliminate the possibility
  of a user trying to change data accidentally
- use `the_collector` to save or retrieve data
    - it uses `msgpack` for efficient data storage and transmission 
- everything has to be lightweight enough to run on a raspberry pi
    - might code in some C stuff for speed if necessary, but I don't think I need it
- used `Process` to get work done and write them in their own file
    - Python's multithreading is not suitable for CPU-bound tasks (because of the GIL),
      so use `multiprocessing`
    - maybe write a simple wrapper to reduce coding
- main program spins up processes for execution on local machine
    - use `Event` to shut things down
    - have simple web server to display plots and camera feed
        - having hard time finding small/fast/simple async python solution to
        stream video/data to multiple users
        - node.js works nice, but then need python -> node bridge (socket.io?)

# Todo

- better incorperation of imagery and cv2 ... shouldn't need to install cv2 to use things
    - how to handle imagery better
- serial-to-matplotlib?
- serial-to-tcp to collect data
- python/c example to use unix domain sockets
- data logger over tcp/unix domain sockets
    - need to have simple setup class to make this easy
    - automatically append time-date
    - put every collect into a folder
    - webpage serve up data
        - show meta data for collect
        - allow deletion of folder/data
        - show available and used hard drive space

# Existing

- [the collector: saving data to files](https://github.com/MomsFriendlyRobotCompany/the_collector)
