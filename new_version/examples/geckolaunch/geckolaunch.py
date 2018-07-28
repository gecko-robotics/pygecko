#!/usr/bin/env python3

"""
So this is sort of a copy of roslaunch
needs to move to bin
"""

import sys
sys.path.append("../../")
from pygecko.transport import GeckoCore
from pygecko.multiprocessing import GeckoProcess
from pygecko.file_storage import FileJson, FileYaml
import multiprocessing as mp
import time
import logging
import logging.config
import logging.handlers
import psutil as psu

# https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes

usage = """------------------------------------------------
Usage:
  geckolaunch launch_file.json

launch_file.json: should be a valid json file detailing where and what
gecko processes to launch.
"""

class Launcher(GeckoProcess):
    def __init__(self, ps):
        GeckoProcess.__init__(self, ps)

    def loop(self):

        self.start()

        try:
            alive = mp.active_children()
            palive = [psu.Process(p.pid) for p in alive]

            while self.event.is_set():
                time.sleep(2)
                print('+', '-'*30, sep='')
                print('| Alive processes:', len(alive))
                print('+', '-'*30, sep='')
                for ps, p in zip(palive, alive):
                    pd = ps.as_dict(attrs=['connections','cpu_percent','memory_percent'])
                    label = '{}[{}]'.format(p.name, p.pid)
                    print('| {:.<30} cpu: {:5}%    mem: {:6.2f}%'.format(label, pd['cpu_percent'], pd['memory_percent']))

        except (KeyboardInterrupt, SystemExit) as e:
            if KeyboardInterrupt == type(e):
                err = 'ctrl-C'
            elif SystemExit == type(e):
                err = 'exit'
            print('\n>> Received {}\n'.format(err))

            # set the kill flag
            self.event.clear()
            time.sleep(0.1)

        finally:
            self.end()


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Error")
        print(usage)
        exit(1)

    reader = FileJson()
    ps = reader.read(sys.argv[1])

    g = Launcher(ps)
    g.loop()
