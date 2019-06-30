##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################
#
# https://pymotw.com/2/socket/multicast.html
#
import socket
import struct
import threading
import time
# import ipaddress  # kjw
from pygecko.pycore.ip import GetIP  # dup?
from pygecko.pycore.transport import Ascii  # , Json, Pickle  # dup?
# import os
import psutil
import multiprocessing as mp


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
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, ttl)
        self.sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)
        self.key = key
        self.host_ip = GetIP().get()
        self.pid = mp.current_process().pid


class BeaconCoreServer(BeaconBase):
    services = {}  # services
    perf = {}
    exit = False
    pubs = {}
    subs = {}
    print = True

    def __init__(self, key, handler=Ascii, ttl=1, addr=None, print=True):
        BeaconBase.__init__(self, key=key, ttl=ttl)

        if addr is not None:
            if len(addr) == 2:
                self.mcast_addr = addr[0]
                self.mcast_port = addr[1]

        # print performance to commandline
        self.print = print

        # setup service socket
        # allow multiple connections
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.sock.bind(('0.0.0.0', self.mcast_port))
        except OSError as e:
            print("*** {} ***".format(e))
            raise

        mreq = struct.pack("=4sl", socket.inet_aton(self.mcast_addr), socket.INADDR_ANY)
        self.sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # setup server data
        self.handler = handler()  # serialization method

        # setup thread
        self.listener = threading.Thread(target=self.printLoop)

    def printLoop(self):
        while not self.exit:
            if self.print:
                self.print()
            time.sleep(3)

    def start(self):
        """Start the listener thread"""
        self.listener.setDaemon(True)
        self.listener.start()

    def stop(self):
        """Stop the listener thread"""
        self.exit = True

    def printProcess(self, pids, bind=False):
        # grab a snapshot of the values
        procs = tuple(pids.values())
        for ps, topic in procs:
            # print(pid)
            # print(ps)
            # print(topic)

            try:
                if ps.is_running():
                    # faster or better?
                    # p.cpu_percent(interval=None)
                    # p.memory_percent(memtype="rss")
                    pd = ps.as_dict(attrs=['connections', 'cpu_percent', 'memory_percent'])
                    # net[psname] = pd['connections']
                    # print(psname, pd['connections'])
                    # cpu = ps.cpu_percent()
                    # cpu = cpu if cpu else -1
                    # mem = ps.memory_percent()
                    # mem = mem if mem else -1
                    label = '[{:>5}] {}'.format(ps.pid, topic)
                    print(' {:.<30} cpu:{:5.1f}%  mem:{:5.1f}%'.format(label, pd['cpu_percent'], pd['memory_percent']))
                    # print('| {:.<30} cpu: {:5}%    mem: {:6.2f}%'.format(label, cpu, mem))
                else:
                    # print('*** remove {} ***'.format(ps.pid))
                    pids.pop(ps.pid)
                    if bind: self.services.pop(topic)
            except Exception as e:
                print("***", e)
                pids.pop(ps.pid)
                if bind: self.services.pop(topic)
        # except:
        #     pids.pop(pid)
        #     pass

    def print(self):
        print(" ")
        print("="*40)
        print(" Geckocore [{}]".format(self.pid))
        print("-------------")
        print(" Key: {}".format(self.key))
        print(" Host IP: {}".format(self.host_ip))
        print(" Listening on: {}:{}".format(self.mcast_addr, self.mcast_port))
        print("-------------")
        print('Known Services [{}]'.format(len(self.services)))
        for k, v in self.services.items():
            print(" * {:.<30} {}".format(k+':', v))

        print("\nBinders [{}]".format(len(self.pubs)))
        self.printProcess(self.pubs, True)

        print("\nConnections [{}]".format(len(self.subs)))
        self.printProcess(self.subs)

        print(" ")

    def handle_sub(self, data):
        # print("handle_sub")
        # print(data)
        # print(self.services.keys())
        ret = None
        topic = data[1]
        pid = int(data[2])
        if topic in self.services.keys():
            endpt = self.services[topic]
            ret = (self.key, topic, endpt,)
            # self.perf[topic] = pid
            # self.subs.append((topic,pid,))
            # self.subs[pid] = topic
            self.subs[pid] = (psutil.Process(pid), topic,)

            print(">> CONN[{}] {}:{}".format(pid, topic, endpt))
        # else:
        #     print("*** handle_sub FAILURE ***")

        # print(">> handle_sub:", ret)

        return ret

    def handle_pub(self, data):
        topic = data[1]
        pid = int(data[2])
        endpt = data[3]

        self.services[topic] = endpt
        # self.perf[topic] = pid
        # self.pubs.append((topic,pid,))
        # self.pubs[pid] = topic
        self.pubs[pid] = (psutil.Process(pid), topic,)

        print(">> BIND[{}] {}:{}".format(pid, topic, endpt))

        return (self.key, topic, endpt, "ok",)

    def callback(self, data, address):
        # print(">> Key: {}".format(self.key))
        # print(">> Address: {}".format(address))
        # print(">> Data: {} size: {}".format(data, len(data)))

        ret = None

        if self.key == data[0]:
            if len(data) == 3: ret = self.handle_sub(data)
            elif len(data) == 4: ret = self.handle_pub(data)
            else: print("*** wtf ***")
        # else:
        #     printf("** Invalid key:", data)

        return ret

    def run(self):
        # self.sock.setblocking(0)

        while not self.exit:
            try:
                data, address = self.sock.recvfrom(1024)
                data = self.handler.loads(data)

                if self.key == data[0]:
                    msg = self.callback(data, address)
                    if msg:
                        msg  = self.handler.dumps(msg)
                        self.sock.sendto(msg, address)
                        # print(">> beacon sent: {}".format(msg))

            except KeyboardInterrupt:
                print("ctrl-z")
                self.exit = True
                return
            except Exception as e:
                print("***", e, "***")
                continue


######################################################


# class BeaconFinder(BeaconBase):
#     """
#     Find Services using the magic of multicast
#
#     pid = 123456
#     proc_name = "my-cool-process"
#     key = hostname
#     finder = BeaconFinder(key)
#     msg = finder.search(msg)
#     """
#     def __init__(self, key, ttl=1, handler=Pickle):
#         BeaconBase.__init__(self, key=key, ttl=ttl)
#         self.handler = handler()
#
#     def send(self, msg):
#         """
#         Search for services using multicast sends out a request for services
#         of the specified name and then waits and gathers responses. This sends
#         one mdns ping. As soon as a responce is received, the function returns.
#         """
#         # serviceName = 'GeckoCore'
#         self.sock.settimeout(self.timeout)
#         # msg = self.handler.dumps((self.key, serviceName, str(pid), processname,))
#         # msg['key'] = self.key
#         msg = self.handler.dumps(msg)
#         self.sock.sendto(msg, self.group)
#         servicesFound = None
#         while True:
#             try:
#                 # data = returned message info
#                 # server = ip:port, which is x.x.x.x:9990
#                 data, server = self.sock.recvfrom(1024)
#                 data = self.handler.loads(data)
#                 # print('>> Search:', data, server)
#                 servicesFound = data
#                 break
#                 # if len(data) == 2:
#                 #     servicesFound = (zmqTCP(server[0], data[0]), zmqTCP(server[0], data[1]),)
#                 #     break
#             except socket.timeout:
#                 print("*** timeout ***")
#                 break
#         # print(">> search done")
#         return servicesFound

#
# class BeaconServer(BeaconBase):
#     """A simple multicast listener which responds to
#     requests for services it has
#
#     # message to be transmitted via multicast
#     msg = {'something': 123, 'other': 'abc'}
#
#     # create a server
#     provider = BeaconServer(
#         'hostname',
#         callback_function [optional],  # ??
#         handler              # ??
#     )
#
#     provider.start()
#     try:
#         while True:
#             time.sleep(500)
#     except KeyboardInterrupt:
#         provider.stop()
#
#     """
#     def __init__(self, key, callback=None, handler=Ascii, ttl=1, addr=None):
#         BeaconBase.__init__(self, key=key, ttl=ttl)
#
#         if addr is not None:
#             if len(addr) == 2:
#                 self.mcast_addr = addr[0]
#                 self.mcast_port = addr[1]
#
#         # setup service socket
#         # allow multiple connections
#         self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         try:
#             self.sock.bind(('0.0.0.0', self.mcast_port))
#             # self.sock.bind((self.mcast_addr, self.mcast_port))
#         except OSError as e:
#             print("*** {} ***".format(e))
#             raise
#
#         mreq = struct.pack("=4sl", socket.inet_aton(self.mcast_addr), socket.INADDR_ANY)
#         self.sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, mreq)
#
#         # setup server data
#         # self.services = {}  # services
#         self.callback = callback
#         self.handler = handler()  # serialization method
#
#         # setup thread
#         # self.exit = False
#         # self.listener = threading.Thread(target=self.listenerThread)
#
#     # def start(self):
#     #     """Start the listener thread"""
#     #     self.listener.setDaemon(True)
#     #     self.listener.start()
#     #
#     # def stop(self):
#     #     """Stop the listener thread"""
#     #     self.exit = True
#     #
#     # def listen(self):
#     #     """TBD"""
#     #     pass
#
#     def run(self):
#         # self.sock.setblocking(0)
#
#         ip = GetIP().get()
#         print("<<< beacon ip: {} >>>".format(ip))
#
#         # while self.exit is False:
#         while True:
#             # print('-'*40)
#             # for k,v in self.services.items():
#             #     print("{}: {}".format(k,v))
#             #
#             # if self.exit is True:
#             #     break
#             # else:
#             # time.sleep(0.2)
#             try:
#                 # time.sleep(0.2)
#                 data, address = self.sock.recvfrom(1024)
#             except KeyboardInterrupt:
#                 print("ctrl-z")
#                 return
#             except Exception:
#                 continue
#
#             data = self.handler.loads(data)
#             # print(">> Address: {}".format(address))
#             # print(">> Data: {}".format(data))
#
#             if self.key == data[0]:
#                 if self.callback:
#                     msg = self.callback(data, address)
#                     # print("MM:",msg)
#                     if msg:
#                         msg  = self.handler.dumps(msg)
#                         self.sock.sendto(msg, address)
#                         # print(">> beacon sent: {}".format(msg))
#                 # else:
#                 #     msg  = self.handler.dumps(('hello',))
#                 #     self.sock.sendto(msg, address)
