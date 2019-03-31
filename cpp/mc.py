#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################

import socket
import struct
import threading
import time
# import ipaddress  # kjw
# from mbeacon.ip import GetIP
# from mbeacon.transport import Ascii, Json, Pickle
import os

class Ascii(object):
    """Simple ASCII format to send info"""
    def dumps(self, data):
        return "|".join(data).encode('utf-8')
    def loads(self, msg):
        return msg.decode('utf-8').split("|")

class BeaconBase(object):
    """
    https://www.tldp.org/HOWTO/Multicast-HOWTO-2.html
    TTL  Scope
    ----------------------------------------------------------------------
       0 Restricted to the same host. Won't be output by any interface.
       1 Restricted to the same subnet. Won't be forwarded by a router.
     <32 Restricted to the same site, organization or department.
     <64 Restricted to the same region.
    <128 Restricted to the same continent.
    <255 Unrestricted in scope. Global.
    """
    mcast_addr = '224.3.29.110'
    mcast_port = 11311
    timeout = 2
    ttl = 1

    def __init__(self, key, ttl=1):
        self.group = (self.mcast_addr, self.mcast_port)
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, ttl)
        self.sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)
        self.key = key

        # print("[Beacon]==================")
        # print(" key: {}".format(self.key))


class BeaconFinder(BeaconBase):
    """
    Find Services using the magic of multicast

    pid = 123456
    proc_name = "my-cool-process"
    key = hostname
    finder = BeaconFinder(key)
    msg = finder.search(msg)
    """
    def __init__(self, key, ttl=1, handler=Ascii):
        BeaconBase.__init__(self, key=key, ttl=ttl)
        self.handler = handler()

    def send(self, msg):
        """
        Search for services using multicast sends out a request for services
        of the specified name and then waits and gathers responses. This sends
        one mdns ping. As soon as a responce is received, the function returns.
        """
        # serviceName = 'GeckoCore'
        self.sock.settimeout(self.timeout)
        # msg = self.handler.dumps((self.key, serviceName, str(pid), processname,))
        # msg['key'] = self.key
        msg = self.handler.dumps(msg)
        # print("msg:", msg)
        self.sock.sendto(msg, self.group)
        servicesFound = None
        while True:
            try:
                # data = returned message info
                # server = ip:port, which is x.x.x.x:9990
                data, server = self.sock.recvfrom(1024)
                data = self.handler.loads(data)
                # print('>> Search:', data, server)
                servicesFound = data
                break
                # if len(data) == 2:
                #     servicesFound = (zmqTCP(server[0], data[0]), zmqTCP(server[0], data[1]),)
                #     break
            except socket.timeout:
                print("*** timeout ***")
                break
        # print(">> search done")
        return servicesFound


if __name__ == '__main__':
    bf = BeaconFinder("local")
    msg = ("local", "aa", "1234", "tcp://1.2.3.4:9000")
    data = bf.send(msg)
    print(data)

    msg = ("local", "aa", "1234")
    data = bf.send(msg)
    print(data)
