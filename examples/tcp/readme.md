# TCP/IP

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

## Uncommon

For simplicity, we create a `GeckoCore` process to route messages between
processes in this program. Typically, you would run `geckocore` from the
command line in a separate window.
