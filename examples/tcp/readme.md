# TCP/IP

# Before Start

You need to run a geckocore before you start this:

    `geckocore.py`

# Description

This uses TCP to move messages between processes.

- `GeckoPy`: Useful functions to setup a function as a process and make things
easier
    - `GeckoPy.Rate()`: returns an object to help throttle your process to a
    specific hertz
    - `GeckoPy.Subscribe()`: creates a subscriber that calls a function when
    a message arrives.
        - `GeckoPy.spin()`: handles the mechanics of checking for messages on
        a topic and then calls the function when one arrives
    - `GeckoPy.Publisher()`: creates a publisher that allows you to publish
    messages to a topic

This does not use `geckolauncher.py`, but just starts a bunch of processes
that call `GeckoPy`.

# Running

Open two windows, in one, run `geckocore.py` and the other run `tcp.py`.
