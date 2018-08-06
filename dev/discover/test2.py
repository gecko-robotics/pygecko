#!/usr/bin/env python3

import socket
import struct
import threading
import time
import ipaddress  # kjw
import pickle
from collections import namedtuple


class GeckoService(object):
    # """Stores variables for a service"""
    # def __init__(self, serviceName, servicePort, serviceIP=""):
    def __init__(self, i, o, f):
        # self.serviceName = serviceName
        # self.servicePort = servicePort
        # self.serviceIP = serviceIP
        self.serviceName = "GeckoCore"
        self.in_addr = i
        self.out_addr = o
        self.info_addr = f

    def pack(self):
        # ourServicePort = self.services[serviceName].servicePort
        # msg = "|".join(("service", str(ourServicePort)))
        # msg.encode('utf-8')
        return pickle.dumps((self.in_addr,self.out_addr,self.info_addr,))

    def unpack(self, msg):
        return pickle.loads(msg)

    def __repr__(self):
        """For printing"""
        # return "%s %s:%s" % (self.serviceName,
        #         str(self.serviceIP),
        #         self.servicePort)
        s = "{}\n  in: {}\n  out: {}\n  info: {}"
        return s.format(self.serviceName, self.in_addr, self.out_addr, self.info_addr)




class serviceFinder(object):
    """Find Services using the magic of multicast"""
    def __init__(self, ip, port, ttl=10):
        self.group = (ip, port)
        self.sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_DGRAM)
        self.sock.setsockopt(
                socket.IPPROTO_IP,
                socket.IP_MULTICAST_TTL,
                struct.pack('b', ttl))
        self.sock.setsockopt(
                socket.SOL_IP,
                socket.IP_MULTICAST_LOOP,
                1)

    def search(self, serviceName, pid, processname):
        """
        Search for services using multicast sends out a request for services
        of the specified name and then waits and gathers responses
        """
        # print("Searching for service '%s'" % serviceName)
        self.sock.settimeout(5)
        msg = "|".join(("findservice", serviceName, str(pid), processname))
        self.sock.sendto(msg.encode('utf-8'), self.group)
        servicesFound = []
        while True:
            try:
                data, server = self.sock.recvfrom(1024)
                data = pickle.loads(data)
                if len(data) == 3:
                    s = GeckoService(*data)
                    servicesFound.append(s)
                    break
            except socket.timeout:
                break
        return servicesFound


class serviceProvider(object):
    """A simple multicast listener which responds to
    requests for services it has"""
    def __init__(self, group, port):
        self.serverAddr = ('0.0.0.0', port)
        self.sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_DGRAM,
                socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.serverAddr)

        mreq = struct.pack("=4sl", socket.inet_aton(group), socket.INADDR_ANY)
        self.sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, 1)
        self.sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)
        self.services = {}
        self.exit = False
        self.ended = threading.Event()

        self.listener = threading.Thread(target=self.listenerThread)

    def start(self):
        self.listener.setDaemon(True)
        self.listener.start()

    def stop(self):
        self.exit = True
        self.ended.wait()

    def addService(self, serv):
        if serv.serviceName not in self.services:
            self.services[serv.serviceName] = serv

    def listenerThread(self):
        self.sock.setblocking(0)
        while True:
            if self.exit == True:
                break
            else:
                time.sleep(0.5)
                try:
                    data, address = self.sock.recvfrom(1024)
                except:
                    continue
                data = data.decode('utf-8').split("|")
                # data = pickle.loads(data)
                print(data)

                if len(data) == 4:
                    cmd = data[0]
                    serviceName = data[1]
                    pid = int(data[2])
                    process_name = data[3]
                    print('{}[{}]'.format(process_name, pid))
                    if cmd == "findservice":
                        if serviceName in self.services:
                            msg = self.services[serviceName].pack()
                            self.sock.sendto(msg, address)

        self.ended.set()


def main():
    import sys
    mcast_addr = '224.3.29.110'
    mcast_port = 9990

    valid = ipaddress.ip_address(mcast_addr).is_multicast
    print("Valid multicast address: {}".format(valid))
    if not valid:
        print("please select a valid multicast address")
        sys.exit(1)

    if len(sys.argv) == 1:
        print("Usage: hxsd [provide|search]")
        sys.exit(1)

    if sys.argv[1] == 'provide':
        if len(sys.argv) != 2:
            print("Usage: hxsd provide")
            exit()

        provider = serviceProvider(mcast_addr, mcast_port)

        s = GeckoService(9998,9999,'/tmp/uds_file')
        provider.addService(s)

        provider.start()
        try:
            while True:
                time.sleep(500)
        except KeyboardInterrupt:
            print("\nShutting things down...")
            provider.stop()

    elif sys.argv[1] == 'search':
        if len(sys.argv) != 3:
            print("usage: hxsd search [service]")
            exit()
        finder = serviceFinder(mcast_addr, mcast_port)
        resp = finder.search(sys.argv[2],11311,"func")
        print(resp)

    # elif sys.argv[1] == 'process':
    #     if len(sys.argv) != 4:
    #         print("usage: hxsd process [pid] [name]")
    #         exit()
    #     finder = serviceFinder(mcast_addr, mcast_port)
    #     finder.process(11238, "bigtest")

if __name__ == "__main__":
    main()
