# Examples

For all examples, you need to have `geckocore` running.

- `geckolaunch`: uses a launch file to start multiple processes
- `tcp`: gecko using TCP/IP to communicate
- `uds`: gecko using unix domain sockets (a file path) to communicate

## Trouble

Sometimes when you are developing stuff with multiple processes, some of them
get left behind (still running). You can find and kill these with `pstree` and
`kill`.

    brew install pstree

Let's see some things running. Lots of python including `Dropbox`.

```bash
kevin@Dalek ~ $ pstree -s python
-+= 00001 root /sbin/launchd
 |-+= 00309 kevin /Applications/Utilities/Terminal.app/Contents/MacOS/Terminal -psn_0_61455
 | \-+= 05608 root login -pfl kevin /bin/bash -c exec -la bash /bin/bash
 |   \-+= 05609 kevin -bash
 |     \-+= 10323 kevin /usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/Resources/Python.app/Co
 |       |--- 10326 kevin /usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/Resources/Python.app/
 |       |--- 10327 kevin /usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/Resources/Python.app/
 |       |--- 10328 kevin /usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/Resources/Python.app/
 |       \--- 10329 kevin /usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/Resources/Python.app/
 |-+= 00491 kevin /Applications/Dropbox.app/Contents/MacOS/Dropbox
 | \--- 00496 kevin /Applications/Dropbox.app/Contents/MacOS/Dropbox -type:exit-monitor -python-version:2.7.11 -method:
 \--- 00495 kevin /Applications/Dropbox.app/Contents/MacOS/Dropbox -type:crashpad-handler --capture-python --no-upload-
```

### Finding and killing leftover processes.

Here I am running a gecko script with the string *zmq* in it. `pstree` allows
me to look for that string and returns the processes associated with it.

```bash
kevin@Dalek ~ $ pstree -s zmq
-+= 00001 root /sbin/launchd
 \--- 17535 kevin /usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Ve
kevin@Dalek ~ $ kill -9 17535
```
