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

from __future__ import print_function
from __future__ import division
import zmq
import socket
# from pygecko.transport.beacon import GetIP

class GetIP(object):
    ip = None
    def get(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            try:
                n = socket.gethostname()
                # make sure it has a zeroconfig .local or you end up
                # with 127.0.0.1 as your address
                if n.find('.local') < 0:
                    n += '.local'
                IP = socket.gethostbyname(n)
            except:
                IP = '127.0.0.1'
        finally:
            s.close()

        self.ip = IP
        return IP

def zmq_version():
    """
    What version of the zmq (C++) library is python tied to?
    """
    print('Using ZeroMQ version: {0!s}'.format((zmq.zmq_version())))


def zmqTCP(host, port):
    """
    Set the zmq address as TCP: tcp://host:port
    """
    if host == 'localhost':  # do I need to do this?
        # host = Socket.gethostbyname(Socket.gethostname())
        host = GetIP().get()
    return 'tcp://{}:{}'.format(host, port)


def zmqUDS(mnt_pt):
    """
    Set the zmq address as a Unix Domain Socket: ipc://file
    """
    return 'ipc://{}'.format(mnt_pt)
