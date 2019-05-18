from __future__ import print_function
import time
import os
from collections import namedtuple
from multiprocessing import Event
# from enum import IntFlag
# import time
from math import pi
# import numpy as np

from pygecko.pycore.mbeacon import BeaconCoreServer
from pygecko.pycore.transport import Ascii

from pygecko.multiprocessing import geckopy
from pygecko.transport import Pub, Sub
from pygecko.transport import zmqTCP
from pygecko.transport import zmqUDS
# from pygecko.transport import GeckoCore
from pygecko.multiprocessing import GeckoSimpleProcess

from pygecko import FileJson, FileYaml

from pygecko.transport.protocols import MsgPack
from pygecko.messages import vec_t, quaternion_t, wrench_t, twist_t, pose_t
from pygecko.messages import imu_st, lidar_st, joystick_st, image_st

# Fake cv2 things for testing
import pygecko.fake.fake_camera as pcv2


def test_messages():
    buffer = MsgPack()

    im = pcv2.cvImage(20, 20)  # fake image

    tests = [
        22,
        "hello world",
        (1, 2, 3),
        # [1,2,3,4],  # lists always => tuples
        {'a': 1, 'b': 3},
        vec_t(1, 2, 3),
        quaternion_t(1, 2, 3, 4),
        wrench_t(vec_t(1, 2, 3), vec_t(4, 5, 6)),
        pose_t(vec_t(1, 2, 3), quaternion_t(4, 5, 6, 7)),
        twist_t(vec_t(1, 2, 3), vec_t(4, 5, 6)),
        imu_st(vec_t(1, 2, 3), vec_t(4, 5, 6), vec_t(7, 8, 9)),
        lidar_st(((1, 2), (3, 4), (5, 6), (7, 8))),
        joystick_st((1, 2, 3), (0, 0, 0, 1), "ps4"),
        image_st(im.shape, im.tobytes(), False)
    ]

    for t in tests:
        m = buffer.pack(t)
        m = buffer.unpack(m)
        assert t == m, "{} => {}".format(t, m)


def test_new_messages():
    """
    Add new messages to pygecko
    """
    class msg_t(namedtuple('msg_t', 'x y z')):
        __slots__ = ()

        def __new__(cls, x, y, z):
            cls.id = 111
            return cls.__bases__[0].__new__(cls, x, y, z)

    def unpack(id, data):
        # unpack new message with id 111
        if id == 111:
            return msg_t(*data)
        return None

    # buffer = MsgPack(list(IntFlag('new', {'msg_t': 111})), unpack)
    buffer = MsgPack([111], unpack)
    m = msg_t(1, 2, 3)
    b = buffer.pack(m)
    b = buffer.unpack(b)
    assert m == b, "{} => {}".format(m, b)


def file_func(Obj, fname):
    data = {'a': 1, 'bob': [1, 2, 3, 4], 'c': "hello cowboy", 'd': {'a': pi}}
    f = Obj()
    f.set(data)
    f.write(fname)
    d = f.read(fname)
    assert d == data
    os.remove(fname)


def test_json():
    file_func(FileJson, 'test.json')


def test_yaml():
    file_func(FileYaml, 'test.yml')


def test_rate():
    rate = geckopy.Rate(10)
    start = time.time()
    for _ in range(10):
        rate.sleep()
    stop = time.time()
    # print(stop - start)
    assert (stop - start) + 0.05 > 1.0


def msg_zmq(args):
    # start message hub
    # core = GeckoCore()
    # core.start()
    bs = BeaconCoreServer(key='test', handler=Ascii)
    bs.start()
    bs.run()

    msg1 = imu_st(
        vec_t(1, 2, 3),
        vec_t(11, 12, 13),
        vec_t(21, 22, 23))

    msg2 = twist_t(
        vec_t(1, 2, 3),
        vec_t(11, 12, 13))

    msg3 = pose_t(
        vec_t(1, 2, 3),
        quaternion_t(1, 2, 3, 4))

    msg4 = lidar_st(
        (
            (1, 1),
            (2, 2),
            (3, 3)
        )
    )

    def publisher(**kwargs):
        geckopy.init_node(**kwargs)
        # p = geckopy.Publisher(topics=['test'])
        # uds = kwargs.get('path')
        p = Pub()
        p.bind(kwargs.get('path'))
        time.sleep(1)  # need this!!

        for msg in [msg1, msg2, msg3, msg4]:
            # for msg in [msg1, msg2]:
            p.publish(msg)
            time.sleep(0.01)

    p = GeckoSimpleProcess()
    p.start(func=publisher, name='publisher', kwargs=args)

    # subscriber
    s = Sub()
    s.topics = args.get('topics')
    s.connect(args.get('path'))

    for msg in [msg1, msg2, msg3, msg4]:
        m = s.recv()
        # assert t == b'test'  # FIXME: fix stupid binary string crap!
        assert msg == m

    # core.join(0.1)
    time.sleep(1)  # if I run these too fast, I get errors on bind()


# def test_msg_zmq_tcp():
#     args = {
#         'path': zmqTCP('localhost', 9999),
#         'topics': 'bob'
#     }
#     msg_zmq(args)
#
#
# def test_msg_zmq_uds():
#     args = {
#         'path': zmqUDS('/tmp/udstest'),
#         'topics': 'bob'
#     }
#     msg_zmq(args)

# bs = BeaconCoreServer(key='test', handler=Ascii)
# core = GeckoSimpleProcess()
# core.start(func=bs.run, name='geckocore')


def zmq_pub_sub(args):
    geckopy.init_node()
    # stop pub
    exit = Event()
    exit.clear()

    msg = imu_st(
        vec_t(1, 2, 3),
        vec_t(11, 12, 13),
        vec_t(21, 22, 23))

    def publisher(**kwargs):
        geckopy.init_node()
        exit = kwargs['exit']

        pt = kwargs["pub"]
        key = kwargs["key"]
        topic = kwargs["topic"]
        if pt == "bindtcp":
            p = geckopy.pubBinderTCP(key, topic)
        elif pt == "connecttcp":
            p = geckopy.pubConnectTCP(key, topic)
        elif pt == "binduds":
            p = geckopy.pubBinderUDS(key, topic, "/tmp/pygecko_test")
        elif pt == "connectuds":
            p = geckopy.pubConnectUDS(key, topic)

        if p is None:
            assert False, "<<< Couldn't get Pub from geckocore >>>"

        for _ in range(100):
            if exit.is_set():
                # print("exit")
                break
            p.publish(msg)
            time.sleep(0.1)

    p = GeckoSimpleProcess()
    args['exit'] = exit
    p.start(func=publisher, name='publisher', kwargs=args)

    st = args["sub"]
    key = args["key"]
    topic = args["topic"]

    if st == "connecttcp":
        s = geckopy.subConnectTCP(key, topic)
    elif st == "bindtcp":
        s = geckopy.subBinderTCP(key, topic)
    elif st == "connectuds":
        s = geckopy.subConnectUDS(key, topic)
    elif st == "binduds":
        s = geckopy.subBinderUDS(key, topic, "/tmp/pygecko_test_2")

    for _ in range(5):
        m = s.recv()

        if m:
            exit.set()
            break
        else:
            print(".", end=" ", flush=True)
            time.sleep(0.1)
    assert msg == m, "{} => {}".format(msg, m)


def test_pub_sub():

    bs = BeaconCoreServer(key='test', handler=Ascii)
    core = GeckoSimpleProcess()
    core.start(func=bs.run, name='geckocore')

    args = {
        'key': 'test',
        'topic': "test-tcp",
        'pub': 'bindtcp',
        'sub': 'connecttcp'
    }
    zmq_pub_sub(args)

    args = {
        'key': 'test',
        'topic': "test-tcp-2",
        'pub': 'connecttcp',
        'sub': 'bindtcp'
    }
    zmq_pub_sub(args)

    args = {
        'key': 'test',
        'topic': "test-uds",
        'pub': 'binduds',
        'sub': 'connectuds'
    }
    zmq_pub_sub(args)

    args = {
        'key': 'test',
        'topic': "test-uds-2",
        'pub': 'connectuds',
        'sub': 'binduds'
    }
    zmq_pub_sub(args)

    bs.stop()
    core.join(0.1)


# def test_ps_uds():
#     args = {
#         'key': 'test',
#         'pub': 'binduds',
#         'sub': 'connectuds'
#     }
#     zmq_pub_sub(args)

# def py_zmq():
#     # start message hub
#     core = GeckoCore()
#     core.start()
#
#     def publisher(**kwargs):
#         geckopy.init_node(**kwargs)
#         p = geckopy.Publisher(topics=['test'])
#         time.sleep(1)
#         msg = {'a':1, 'b':[1,2,3], 'c':'hello cowboy'}
#         p.pub('test', msg)  # topic msg
#
#     args = {'host': "localhost"}
#     p = GeckoSimpleProcess()
#     p.start(func=publisher, name='publisher', kwargs=args)
#
#     # subscriber
#     s = Sub(topics=['test'])
#     s.connect(sub_addr)
#     t, msg = s.recv()
#
#     assert t == b'test'
#     assert msg == {'a':1, 'b':[1,2,3], 'c':'hello cowboy'}
#
#     core.join(0.1)
#     time.sleep(1)  # if I run these too fast, I get errors on bind()
#
#
# def test_py_zmq_tcp():
#     py_zmq()


# def test_py_zmq_uds():
#     py_zmq(uds_ifile, uds_ofile)


# def py_geckpy(pub_addr, sub_addr):
#     # start message hub
#     core = GeckoCore(pub_addr, sub_addr)
#     core.start()
#
#     geckopy = GeckoPy()
#
#     def callback(t, msg):
#         assert t == b'test'
#         assert msg == {'a':1, 'b':[1,2,3], 'c':'hello cowboy'}
#
#     def callback(**kwargs):
#         addr = kwargs.get('addr')
#         p = Pub()
#         p.connect(addr)
#         time.sleep(1)
#         msg = {'a':1, 'b':[1,2,3], 'c':'hello cowboy'}
#         p.pub('test', msg)  # topic msg
#
#
#
#     args = {'addr': pub_addr}
#     p = GeckoSimpleProcess()
#     p.start(func=publisher, name='publisher', kwargs=args)
#
#     # subscriber
#     s = Sub(topics=['test'])
#     s.connect(sub_addr)
#     t, msg = s.recv()
#
#     print(t, msg)
#
#     assert t == b'test'
#     assert msg == {'a':1, 'b':[1,2,3], 'c':'hello cowboy'}
#
#     p.join(0.1)
#     core.join(0.1)
#
# def test_py_geckopy_tcp():
#     py_geckpy(tcp_pub, tcp_sub)
#
#
# def test_py_geckopy_uds():
#     py_geckpy(uds_ifile, uds_ofile)
