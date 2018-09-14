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
    queue_size=5
    # def __init__(self):
    #     # self.pub = geckopy.Publisher(None, self.queue_size, False)
    #     # if addr is None:  # FIXME: check if geckopy exists!!
    #     #     addr = geckopy.core_inaddr
    #     # self.pub.connect(addr, queue_size=queue_size)
    def run(self):
        """
        this gets called once each time through the loop
        """
        pass

    def spin(self, hertz=20):
        """
        this spins until killed
        """
        self.pub = geckopy.Publisher(None, self.queue_size, False)
        rate = geckopy.Rate(hertz)
        while not geckopy.kill:
            run()
            rate.sleep()


class Source(Publisher):
    pass
#    def __init__(self, addr=None, queue_size=5):
#        Publisher.__init__(self,addr=None, queue_size=5)



"""
from gecko import geckopy

class RobotCommand(Sink):
    def __init__(self):
        self.robot = Robot()

    def callback(self, topic, msg):
        if topic == b'cmd':
            geckopy.log("{}: {}".format(topic,msg))
            robot.command(msg)
        elif topic == b'a':
            print('hi')


def function(**kwargs):
    geckopy.init_node(**kwargs)

    rc = RobotCommand(topics=['a', 'cmd'])
    geckopy.spin()

"""



class Subscriber(object):
    def __init__(self, topics):
        # create subscriber and push into geckopy.subs loop
        # gecko
        geckopy.Subscriber(topics, self.callback, None, False)
        # conntect
        # setup self.callback
        # push to geckopy.subs
    def callback(self, t, m):
        """
        this gets called once each time a message arrives
        """
        pass


class Sink(Subscriber):
    pass


class Rep(object):
    def __init__(self, addr):
        self.rep = 3

# this doesn't work:
#   pub.spin()
#   geckopy.spin()
# both can't go at same time!!!
# """
# class Range(Filter):
#     def callback(self, t, m):
#         if t == b'scan':
#             # do something
#             self.pub('new-topic', m)
#
# r = Range('topic'):
# r.spin()
# """
# class Filter(Subscriber, Publisher):
#     """Proxy?"""
#     def __init__(self):
#         Source.__init__(self, pub_addr)
#         Sink.__init__(self, sub_topics, sub_addr)
#
#
# class Relay(Sink, Rep):
#     """Device?"""
#     def __init__(self, topics, rep_addr, sub_addr=None):
#         Sink.__init__(self, topics, sub_addr)
#        Rep.__init__(self, rep_addr)




# import signal
#
#
# class SignalCatch(object):
#     """
#     Catches SIGINT and SIGTERM signals and sets kill = True
#
#     https://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully
#     """
#     kill = False
#     def kill_signals(self):
#         signal.signal(signal.SIGINT, self.exit_gracefully)
#         signal.signal(signal.SIGTERM, self.exit_gracefully)
#
#     def exit_gracefully(self, signum, frame):
#         """
#         When handler gets called, it sets the self.kill to True
#         """
#         self.kill = True
#         # print(">> Got signal[{}], kill = {}".format(signum, self.kill))

# class Filter(object):
#     """
#     Relay?
#     value?
#
#     def func(t, m):
#         print(t,m)
#
#     f = Filter('imu', func)
#     """
#     def __init__(self, in_topics, func, in_addr=None, out_addr=None):
#         global g_geckopy
#         if in_addr is None:
#             in_addr = g_geckopy.core_outaddr
#         if out_addr is None:
#             out_addr = g_geckopy.core_inaddr
#
#         self.func = func
#
#         # out
#         self.pub = Pub()
#         self.pub.connect(out_addr, queue_size=queue_size)
#
#         # in
#         self.sub = Sub(cb_func=self.handle_msg, topics=in_topics)
#         self.sub.connect(in_addr)
#         g_geckopy.subs.append(self.sub)
#
#     def handle_msg(self, topic, msg):
#         t, m = self.func(topic, msg)
#         self.pub(t, m)
#
#
# class Relay(object):
#     """
#     value?
#
#     def a(t,m,state): return state
#     def b(m): return msg
#
#     r = Relay('imu', geckoTCP('localhost', 10000))
#     r.spin(a,b)
#     """
#     def __init__(self, topics, rep_addr, in_addr=None):
#         global g_geckopy
#
#         if in_addr is None:
#             in_addr = g_geckopy.core_outaddr
#         # out
#         # self.pub = Pub()
#         # self.pub.connect(out_addr, queue_size=queue_size)
#
#         # in
#         self.sub = Sub(cb_func=None, topics=topics)
#         self.sub.connect(in_addr)
#
#         # reply
#         self.rep = Reply()
#         self.rep.bind(rep_addr)
#
#     def spin(self, msg_func, rep_func, hertz=10):
#         global g_geckopy
#         rate = geckopy.Rate(hertz)
#         state = None
#         while not g_geckopy.kill:
#             topic, msg = self.sub.recv_nb()
#             if topic:
#                 state = msg_func(topic, msg, state)
#
#             msg = self.rep.listen_nb()
#             if msg:
#                 msg = rep_func(msg, state)
#                 self.rep.reply(msg)
#
#             rate.sleep()
#
#
# class Sink(object):
#     """
#     value?
#     """
#     def __init__(self, func, in_topics, addr=None):
#         global g_geckopy
#
#         if addr is None:
#             addr = g_geckopy.core_outaddr
#
#         # in
#         self.sub = Sub(cb_func=func, topics=in_topics)
#         self.sub.connect(addr)
#         g_geckopy.subs.append(self.sub)
#
#
#
# class Source(object):
#     def __init__(self, addr=None):
#         global g_geckopy
#
#         self.pub = Pub()
#         if addr is None:
#             addr = g_geckopy.core_inaddr
#
#         # if bind:
#         #     p.bind(addr, queue_size=queue_size)
#         # else:
#         self.pub.connect(addr, queue_size=queue_size)
#
#     def spin(self, func, topic, hertz):
#         global g_geckopy
#         rate = geckopy.Rate(hertz)
#         while not g_geckopy.kill:
#             msg = func()
#             self.pub(topic, msg)
#             rate.sleep()
