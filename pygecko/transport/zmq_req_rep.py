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
import time
from pygecko.transport.zmq_base import Base


class Rep(Base):
    """
    Reply?
    """
    def __init__(self):
        Base.__init__(self)
        self.socket = self.ctx.socket(zmq.REP)

    def __del__(self):
        """
        wtf! I need this or it hangs
        """
        self.close()

    def listen(self, callback, flags=0):
        """
        checks to see if a request needs to be serviced
        callback: a function to handle a request message and return the answer.
            The function must be able to handle a message it didn't expect.
            Since there are no topics associated with this, a user might send
            some crazy message

            callback(message) -> answer

        returns True if serviced, False if not
        """
        # print 'listen'
        ret = False
        try:
            jmsg = self.socket.recv_multipart(flags=flags)[0]
            msg = self.pickle.unpack(jmsg)
            # print("*** {} ***".format(msg))

            msg = callback(msg)

            jmsg = self.pickle.pack(msg)
            self.socket.send(jmsg)
            ret = True

        except zmq.Again as e:
            # no response yet or server not up and running yet
            # time.sleep(0.001)
            # print("*** no reply ***")
            pass
        except Exception:
            # something else is wrong
            raise

        return ret

    def listen_nb(self, callback, flags=0):
        """

        """
        return self.listen(callback=callback, flags=zmq.NOBLOCK)
        # while True:
        #     jmsg = self.socket.recv_multipart()[0]
        #     msg = self.pickle.unpack(jmsg)
        #
        #     msg = callback(msg)
        #
        #     jmsg = self.pickle.pack(msg)
        #     self.socket.send(jmsg)

    # def listen_nb(self, callback):
    #     """
    #     checks to see if a request needs to be serviced
    #     callback: a function to handle a request message and return the answer.
    #         The function must be able to handle a message it didn't expect.
    #         Since there are no topics associated with this, a user might send
    #         some crazy message
    #
    #         callback(message) -> answer
    #
    #     returns True if serviced, False if not
    #     """
    #     # print 'listen'
    #     ret = False
    #     try:
    #         jmsg = self.socket.recv_multipart(flags=zmq.NOBLOCK)[0]
    #         msg = self.pickle.unpack(jmsg)
    #         # print("*** {} ***".format(msg))
    #
    #         msg = callback(msg)
    #
    #         jmsg = self.pickle.pack(msg)
    #         self.socket.send(jmsg)
    #         ret = True
    #
    #     except zmq.Again as e:
    #         # no response yet or server not up and running yet
    #         # time.sleep(0.001)
    #         # print("*** no reply ***")
    #         pass
    #     except Exception:
    #         # something else is wrong
    #         raise
    #
    #     return ret
    #
    # def listen(self, callback, flags=0):
    #     """
    #     The same as listen_nb() but this one blocks until a request is made.
    #
    #     this blocks ... utility?
    #     """
    #     while True:
    #         jmsg = self.socket.recv_multipart()[0]
    #         msg = self.pickle.unpack(jmsg)
    #
    #         msg = callback(msg)
    #
    #         jmsg = self.pickle.pack(msg)
    #         self.socket.send(jmsg)


class Req(Base):
    """
    Request?
    """
    def __init__(self):
        Base.__init__(self)
        self.socket = self.ctx.socket(zmq.REQ)

    def __del__(self):
        """Calls Base.close()"""
        self.close()

    def get_nb(self, msg):
        """
        Calls get(flags) with flags=zmq.NOBLOCK to implement non-blocking
        (or zmq.DONTWAIT). If no answer is received, then None is returned.
        """
        return self.get(msg, flags=zmq.NOBLOCK)

    def get(self, msg, flags=0):
        """
        Implements recv_multipart(flags) with flags=0 for non-blocking.
        """
        jmsg = self.pickle.pack(msg)
        msg = None
        self.socket.send(jmsg)
        try:
            jmsg = self.socket.recv_multipart(flags=flags)[0]
            msg = self.pickle.unpack(jmsg)
        except zmq.Again as e:
            # no response yet or server not up and running yet
            time.sleep(0.001)
        except Exception as e:
            # something else is wrong
            raise
        return msg
