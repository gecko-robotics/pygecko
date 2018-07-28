##############################################
# The MIT License (MIT)
# Copyright (c) 2014 Kevin Walchko
# see LICENSE for full details
##############################################
#
# Kevin J. Walchko 13 Oct 2014
#
# see http://zeromq.org for more info
# http://zguide.zeromq.org/py:all
#
# kevin@Dalek ~ $ pstree -s zmq
# -+= 00001 root /sbin/launchd
#  \--- 17535 kevin /usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Ve
# kevin@Dalek ~ $ kill -9 17535
#

from __future__ import print_function
from __future__ import division
import zmq
from zmq.devices import ProcessProxy
import multiprocessing as mp
import time
# import socket as Socket
from pygecko.transport.helpers import zmqTCP, zmqUDS
from pygecko.transport.zmqclass import Pub, Sub
import signal


# class Core(object):
#     """
#     http://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/devices/forwarder.html
#     """
#     def __init__(self, inaddr=None, outaddr=None):
#         core = ProcessProxy(zmq.SUB, zmq.PUB)
#         self.core = core
#
#         if inaddr is None:
#             inaddr = zmqTCP('localhost', 9998)
#         if outaddr is None:
#             outaddr = zmqTCP('localhost', 9999)
#
#         # inputs (sub)
#         core.bind_in(inaddr)
#         core.setsockopt_in(zmq.SUBSCRIBE, b'')
#
#         # outputs (pub)
#         core.bind_out(outaddr)
#         core.start()
#
#         print('+', '-'*30, sep='')
#         print('| Core')
#         print('+', '-'*30, sep='')
#         # print("core:", core)
#         print('|  In[sub]: {}'.format(inaddr))
#         print('|  Out[pub]: {}'.format(outaddr))
#         print('+', '-'*30, sep='')
#
#     def __del__(self):
#         # self.input.close()
#         # self.out.close()
#         # self.ctx.term()
#         self.core.join(1)
#         print("Core exiting")
#
#     def join(self, timeout=1):
#         self.core.join(timeout)
#
# class GeckoCore(Core):
#     pass
