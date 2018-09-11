# :lizard:  pyGecko

## My robot software.

- Doesn't use [ROS](http://ros.org), ROS is a pain to install and maintain
on macOS and various linux systems
    - Uses some of the same ideas, constructs, architecture ideas, APIs but
    not strictly adhering to them
- Uses [Zero MQ](http://http://zeromq.org/) as the inter-process communication
(uses both TCP and UDS) instead of RPC-XML
    - looked at Google's protobuf, but was more complex than I needed
    - using [`msgpack`](https://msgpack.org/index.html) to serialize data
    - instead of `roscore` use `geckocore.py` as the message hub
        - produce performance data (see below)
    - instead of `roslaunch` use `geckolaunch.py`
        - produces performance data (see below)
- Uses [`the_collector`](https://github.com/MomsFriendlyRobotCompany/the_collector)
to save/retrieve data to a file
- `simplejson`/`pyyaml` - config and launch files
- All of this runs on [Raspberry Pi 3](http://www.raspberrypi.org)

# Architecture

```bash
                                geckocore
              spawn | pub --\  +---------+  /---> sub
geckolaunch ------->| pub ---->|in    out|------> sub
                    | pub --/  +---------+  \---> sub
                                             \--> sub
```

- Any number of pubs can talk to any number of sub ... it is not a one-to-one relationship.
- Subscriber can subscribe to multiple topics
- Publishers are not bound to any one topic, but can also publish to multiple topics

## `geckocore.py`

This is the main message hub and keeps track of messages statistics that pass
through it along with connections.

```bash
+------------------------------------------------------------
| GeckoCore[32871].............. cpu:   6.7%    mem:   0.06%
| Total messages seen: 1058
+------------------------------
| LISTEN 192.168.86.213:9998 connected to None:None
| LISTEN 192.168.86.213:9999 connected to None:None
| ESTABLISHED 192.168.86.213:9998 connected to 192.168.86.213:49793
| ESTABLISHED 192.168.86.213:9998 connected to 192.168.86.213:49792
| ESTABLISHED 192.168.86.213:9999 connected to 192.168.86.213:49794
| ESTABLISHED 192.168.86.213:9999 connected to 192.168.86.213:49795
| ESTABLISHED 192.168.86.213:9999 connected to 192.168.86.213:49796
| ESTABLISHED 192.168.86.213:9999 connected to 192.168.86.213:49797
| ESTABLISHED 192.168.86.213:9999 connected to 192.168.86.213:49798
| ESTABLISHED 192.168.86.213:9999 connected to 192.168.86.213:49799
| ESTABLISHED 192.168.86.213:9998 connected to 192.168.86.213:49800
+------------------------------
 hello.........................   39.3 msgs/s      1.8 kB/s
 hey there.....................   39.3 msgs/s      1.8 kB/s
 cv............................   14.3 msgs/s   4298.6 kB/s
```
geckocore also is passed the PIDs for processes on the local machine and
prints performance data on each process:

```bash
+------------------------------
| Alive processes: 9
+------------------------------
| subscribe2[32880]............. cpu:   3.5%    mem:   0.07%
| subscribe2[32882]............. cpu:   3.5%    mem:   0.07%
| subscribe2[32885]............. cpu:   2.2%    mem:   0.08%
| subscribe2[32884]............. cpu:   2.2%    mem:   0.08%
| pcv[32886].................... cpu:   5.7%    mem:   0.18%
| subscribe2[32881]............. cpu:   3.5%    mem:   0.07%
| subscribe2[32883]............. cpu:   3.4%    mem:   0.07%
| publish[32879]................ cpu:   0.9%    mem:   0.07%
| publish[32878]................ cpu:   0.9%    mem:   0.07%
```

Note that the topics above are: `hello`, `hey there`, and `cv`. They can be any string.

## `geckolaunch.py`

`geckolaunch.py` allows you to launch a bunch of processes quickly using a launch
file. A launch file is just a simple json file where each line takes the form:
`[file, function, kwargs]`. Here is an example:

```bash
{
  "processes":
  [
    ["process", "publish", {"topic": "hello"}],
    ["process", "publish", {"topic": "hey there"}],
    ["process", "subscribe2", {"topic": "hello"}],
    ["process", "subscribe2", {"topic": "hello"}],
    ["process", "subscribe2", {"topic": "hey there"}],
    ["process", "subscribe2", {"topic": "hey there"}],
    ["process", "subscribe2", {"topic": "cv"}],
    ["process", "subscribe2", {"topic": "cv"}],
    ["process", "pcv", {"topic": "cv"}]
  ]
}
```

Here we have a bunch of functions (`publish`,  `subscribe2`, and `pcv`) located in a
python file called `process.py` (note, the `.py` file extension is assumed because
`pygecko` uses `import` to load these functions. There is no reason eveything has
to be located in one file, I was just lazy when I wrote this example and did
a lot of copy/paste. :smile:

There are a bunch of `kwargs` (dictionaries) that are passed to the functions full
of whatever args you want to pass. In this example, the args are mostly just
topic names to pub/sub to.

## `geckopy`

See the examples, but this acts like a `rospy` and helps make writing
pub/sub processes easy. See the `/examples` folder to see it in action.

- **init_node:** this sets up the the process for communications with `geckocore`
- **log:** prints log messages
    ```python
    from pygecko import geckopy, Log
    geckopy.loginfo('this is a info message')
    geckopy.logwarn('this is a warning message')
    geckopy.logerror('this is a error message')
    geckopy.logdebug('this is a debug message')
    ```
- **on_shutdown:** pushes a function to a stack (FIFO) that will be called when `geckopy`
shutsdown
- **Subscriber:** creates a subscriber and appends the callback function to an
array in geckopy
- **Publisher:** creates a publisher and returns it
- **Rate:** given a frequency of how often a loop should run (i.e., 10Hz), the
returned object will dynamically set the sleep interval to achieve the rate. Ex:
    ```python
    from pygecko import geckopy
    rate = geckopy.Rate(20)  # run loop at 20 Hz
    while True:
        rate.sleep()
    ```

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
