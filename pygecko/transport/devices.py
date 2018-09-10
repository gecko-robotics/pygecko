from pygecko.multiprocessing import geckopy
from pygecko.transport import zmqTCP
from pygecko.transport.zmq_base import ZMQError
from pygecko.transport.zmq_sub_pub import Pub, Sub  #, SubNB
from pygecko.transport.zmq_req_rep import Req

# from pygecko.multiprocessing import g_geckopy


"""
from gecko import geckopy

class Test(Source):
    def __init__(self):
        self.imu = IMU()
        
    def run(self):
        a,g,m = self.imu.read()
        msg = IMU(a,g,m)
        self.pub.pub('test', msg)
        geckopy.log('sent msg')


def function(**kwargs):
    geckopy.init_node(**kwargs)
    
    t = Test()
    t.spin(10)  # 10 Hz

"""


class Publisher(object):
    """

    """
    def __init__(self, addr=None, queue_size=5):
        self.pub = geckopy.Publisher(addr, queue_size, False)
        # if addr is None:  # FIXME: check if geckopy exists!!
        #     addr = geckopy.core_inaddr
        # self.pub.connect(addr, queue_size=queue_size)
    def run(self):
        """
        this gets called once each time through the loop
        """
        pass
    def spin(self, hertz=20):
        """
        this spins until killed
        """
        rate = geckopy.Rate(hertz)
        while not geckopy.kill:
            run()
            rate.sleep()


class Source(Publisher):
    pass
#    def __init__(self, addr=None, queue_size=5):
#        Publisher.__init__(self,addr=None, queue_size=5)


class Sink(object):
    def __init__(self, topics, addr):
        # create subscriber and push into geckopy.subs loop
        geckopy.Subscriber(topics, self.callback, addr, False)
        # conntect
        # setup self.callback
        # push to geckopy.subs
    def callback(self, t, m):
        """
        this gets called once each time a message arrives
        """
        pass


class Rep(object):
    def __init__(self, addr):
        self.rep = 3


class Filter(Source, Sink):
    """Proxy?"""
    def __init__(self, sub_topics, sub_addr=None, pub_addr=None, queue_len=5):
        Source.__init__(self, pub_addr)
        Sink.__init__(self, sub_topics, sub_addr)


class Relay(Sink, Rep):
    """Device?"""
    def __init__(self, topics, rep_addr, sub_addr=None):
        Sink.__init__(self, topics, sub_addr)
        Rep.__init__(self, rep_addr)

