##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################
from pygecko.transport.helpers import zmqTCP
from pygecko.transport.beacon import get_host_key
from mbeacon import BeaconFinder
from pygecko.transport.zmq_sub_pub import Pub
import time


class CoreFinder(object):
    """
    This uses various methods to find the address of geckocore
    """
    core_inaddr = None
    core_outaddr = None
    start_core = False

    def __init__(self, pid, name, **kwargs):
        self.pid = pid
        self.name = name

        if 'geckocore' in kwargs:
            core = kwargs['geckocore']

            # outright tell it the address
            # if 'type' in core:
            #     if core['type'].lower() == 'tcp':
            #         ain = core['in']
            #         aout = core['out']
            #         self.core_inaddr = zmqTCP(*ain)
            #         self.core_outaddr = zmqTCP(*aout)
            #     elif core['type'].lower() == 'uds':
            #         raise NotImplementedError('uds not implemented yet')
            #     elif core['type'].lower() == 'loopback':
            #         # self.core_inaddr = zmqTCP('127.0.0.1', 9998)  # or localhost?
            #         # self.core_outaddr = zmqTCP('127.0.0.1', 9999)
            #         self.set_address('127.0.0.1', 9998, 9999)
            #
            #     self.notify_core()  # send pid/name using pub
            #
            #     print("[kwargs]================\n in: {}\n out: {}\n".format(self.core_inaddr, self.core_outaddr))
            # use multicast to find geckocore
            if 'key' in core:
                key = core['key']
                finder = BeaconFinder(key)
                resp = finder.search(pid, name)
                if resp:
                    print("[multicast]================\n in: {}\n out: {}\n".format(*resp))
                    self.core_inaddr = resp[0]
                    self.core_outaddr = resp[1]
                else:
                    # self.core_inaddr = zmqTCP('localhost', 9998)
                    # self.core_outaddr = zmqTCP('localhost', 9999)
                    print("<<< multicast fail >>>")
                    exit(1)
                    # self.set_address('localhost', 9998, 9999)
            else:
                raise Exception("geckoopy: kwargs has incorrect format")
        # all else failed, use the default
        else:
            # need to check for /tmp/gecko*.json
            if False:
                print("[corefile]================\n in: {}\n out: {}\n".format(self.core_inaddr, self.core_outaddr))
            else:
                # self.core_inaddr = zmqTCP('localhost', 9998)
                # self.core_outaddr = zmqTCP('localhost', 9999)
                self.set_address('localhost', 9998, 9999)

            self.notify_core()  # send pid/name using pub

        # WARNING: how do I prevent multiple cores from being launched????
        # if 'start_core' in kwargs:
        #     if kwargs['start_core'] == True:
        #         self.start_core = True
        #         # raise NotImplementedError('launching core not implemented yet')

    def set_address(self, h, pin, pout):
        self.core_inaddr = zmqTCP(h, pin)
        self.core_outaddr = zmqTCP(h, pout)

    def notify_core(self, retry=3):
        """
        Pass info to geckocore:
            {'proc_info': (pid, name, status)}

            psutil returns name as python for everything. It doesn't know about
            the multiprocessing.Process.name

            status: [remove, unnecessary]
                True: proc up and running
                False: proc is dead
        """
        msg = {'proc_info': (self.pid, self.name, True,)}
        # print(msg)

        # add a Sub() and get an ok from core???
        # create a pub for sending log messages
        # HOWEVER, for right now, reuse it to send process info
        pub = Pub()
        # self.logpub.connect(zmqTCP('localhost', 9998), queue_size=1)
        pub.connect(self.core_inaddr, queue_size=1)
        for _ in range(retry):
            pub.pub('core_info', msg)
            time.sleep(0.1)
"""
if 'geckocore' in self.ps:
    if 'type' in self.ps['geckocore']:
        kind = self.ps['geckocore']['type']
        if kind == 'tcp':
            h, p = self.ps['geckocore']['in']
            in_addr = zmqTCP(h, p)
            h, p = self.ps['geckocore']['out']
            out_addr = zmqTCP(h, p)
        elif kind == 'uds':
            f = self.ps['geckocore']['in']
            in_addr = zmqUDS(f)
            f = self.ps['geckocore']['out']
            out_addr = zmqUDS(f)
    elif 'key' in self.ps['geckocore']:
        key = self.ps['geckocore']['key']
        if key == "localhost":
            key = get_host_key()
            print("<<< Using multicast key: {} >>>".format(key))
        finder = BeaconFinder(key)
        resp = finder.search(0, '0')
        if resp:
            in_addr = resp[0]
            out_addr = resp[1]
        else:
            print("<<< no multicast beacon response >>>")
            in_addr = zmqTCP('localhost', 9998)
            out_addr = zmqTCP('localhost', 9999)
else:
    in_addr = zmqTCP('localhost', 9998)
    out_addr = zmqTCP('localhost', 9999)
"""
