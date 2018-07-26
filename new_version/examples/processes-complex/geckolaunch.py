#!/usr/bin/env python3

"""
So this is sort of a copy of roslaunch
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

# https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes


class Test(GeckoProcess):
    def __init__(self, ps):
        GeckoProcess.__init__(self, ps)

    def loop(self):

        core = GeckoCore()
        # q = Queue()

        d = {
            'version': 1,
            'formatters': {
                'detailed': {
                    'class': 'logging.Formatter',
                    'format': '%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'INFO',
                },
                'file': {
                    'class': 'logging.FileHandler',
                    'filename': 'mplog.log',
                    'mode': 'w',
                    'formatter': 'detailed',
                },
                'foofile': {
                    'class': 'logging.FileHandler',
                    'filename': 'mplog-foo.log',
                    'mode': 'w',
                    'formatter': 'detailed',
                },
                'errors': {
                    'class': 'logging.FileHandler',
                    'filename': 'mplog-errors.log',
                    'mode': 'w',
                    'level': 'ERROR',
                    'formatter': 'detailed',
                },
            },
            'loggers': {
                'foo': {
                    'handlers': ['foofile']
                }
            },
            'root': {
                'level': 'DEBUG',
                'handlers': ['console', 'file', 'errors']
            },
        }
        # logging.config.dictConfig(d)

        self.start()

        try:
            # logger = logging
            while self.event.is_set():
                time.sleep(1)
                alive = mp.active_children()
                print('-'*30)
                print('Alive processes:', len(alive))
                for p in alive:
                   print('  ', p.name, p.pid)
                # debugging info here via print or logging or webpage
                # record = q.get()
                # if record:
                #     logger.handle(record)
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
            core.join(1)


if __name__ == '__main__':
    # if you read in a json file
    # ps = {
    #     # file, function, args
    #     'processes': [
    #         ('process', 'runable_process', {'a':1, 'b':2},),
    #         ('process', 'runable_process',),
    #         ('process', 'runable_process', None,),
    #     ]
    # }
    from pprint import pprint

    reader = FileJson()
    ps = reader.read('launch.json')
    pprint(ps)

    g = Test(ps)
    g.loop()
