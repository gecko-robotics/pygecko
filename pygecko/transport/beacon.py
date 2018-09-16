# https://pymotw.com/2/socket/multicast.html
import socket
import struct
import threading
import time
# import ipaddress  # kjw
import pickle
# from collections import namedtuple
from pygecko.transport.helpers import zmqTCP
# from pygecko.transport.helpers import zmqUDS
import os

try:
    import simplejson as json
except ImportError:
    import json


def get_host_key():
    return os.uname().nodename.split('.')[0].lower()


class Ascii(object):
    """Simple ASCII format to send info"""
    def dumps(self, data):
        return "|".join(data).encode('utf-8')
    def loads(self, msg):
        return msg.decode('utf-8').split("|")

class Json(object):
    """Use json to transport message"""
    def dumps(self, data):
        return json.dumps(data).encode('utf-8')
    def loads(self, msg):
        return json.loads(msg.decode('utf-8'))

class Pickle(object):
    """Use pickle to transport message"""
    def dumps(self, data):
        return pickle.dumps(data)
    def loads(self, msg):
        return pickle.loads(msg)


class GeckoService(object):
    def __init__(self, i, o):
        self.serviceName = "GeckoCore"
        self.in_addr = i
        self.out_addr = o

    def as_tuple(self):
        # return (self.in_addr, self.out_addr, self.info_addr,)
        return (self.in_addr, self.out_addr,)

    # def __repr__(self):
    #     """For printing"""
    #     # s = "{} [{}]\n  in: {}\n  out: {}\n  info: {}"
    #     s = "{} [{}]\n  in: {}\n  out: {}"
    #     return s.format(self.serviceName, self.ip, self.in_addr, self.out_addr,)
    #     # return s.format(self.serviceName, self.ip, self.in_addr, self.out_addr, self.info_addr)


class Beacon(object):
    mcast_addr = '224.3.29.110'
    mcast_port = 11311



class BeaconFinder(Beacon):
    """Find Services using the magic of multicast

    finder = BeaconFinder()
    info = (11311,"func",)
    resp = finder.search(11311,"func")
    """
    def __init__(self, key, ttl=10, handler=Pickle):
        self.group = (self.mcast_addr, self.mcast_port)
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
        self.handler = handler()
        self.key = key

    def search(self, pid, processname):
        """
        Search for services using multicast sends out a request for services
        of the specified name and then waits and gathers responses. This sends
        one mdns ping. As soon as a responce is received, the function returns.
        """
        serviceName = 'GeckoCore'
        self.sock.settimeout(5)
        msg = self.handler.dumps((self.key, serviceName, str(pid), processname,))
        self.sock.sendto(msg, self.group)
        servicesFound = None
        while True:
            try:
                # data = returned message info
                # server = ip:port, which is x.x.x.x:9990
                data, server = self.sock.recvfrom(1024)
                data = self.handler.loads(data)
                if len(data) == 2:
                    servicesFound = (zmqTCP(server[0], data[0]), zmqTCP(server[0], data[1]),)
                    break
            except socket.timeout:
                break
        return servicesFound


class BeaconServer(Beacon):
    """A simple multicast listener which responds to
    requests for services it has

    provider = BeaconServer(
        GeckoService(9998, 9999),
        'findservice'
    )

    provider.start()
    try:
        while True:
            time.sleep(500)
    except KeyboardInterrupt:
        provider.stop()

    """
    def __init__(self, service, key, handler=Pickle):
        ip = self.get_ip()
        self.serverAddr = (ip, self.mcast_port)
        self.sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_DGRAM,
                socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.sock.bind(self.serverAddr)
        except OSError as e:
            print("*** {} ***".format(e))
            # self.sock.bind(self.serverAddr)
            raise

        mreq = struct.pack("=4sl", socket.inet_aton(self.mcast_addr), socket.INADDR_ANY)
        self.sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, 1)
        self.sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)
        self.service = service
        self.exit = False
        self.handler = handler()

        self.listener = threading.Thread(target=self.listenerThread)
        self.key = key

    def start(self):
        self.listener.setDaemon(True)
        self.listener.start()

    def stop(self):
        self.exit = True

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()

        # self.ip = IP
        return IP

    def listenerThread(self):
        self.sock.setblocking(0)

        msg = self.service.as_tuple()
        msg = self.handler.dumps(msg)

        while True:
            if self.exit is True:
                break
            else:
                time.sleep(0.2)
                try:
                    data, address = self.sock.recvfrom(1024)
                except Exception:
                    continue

                data = self.handler.loads(data)
                # print(data)

                if len(data) == 4:
                    key = data[0]
                    serviceName = data[1]
                    # pid = int(data[2])
                    # process_name = data[3]
                    # print('{}[{}]'.format(process_name, pid))
                    if key == self.key:
                        if serviceName == self.service.serviceName:
                            # msg = self.service.as_tuple()
                            # msg = self.handler.dumps(msg)
                            self.sock.sendto(msg, address)
