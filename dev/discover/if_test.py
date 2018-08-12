#!/usr/bin/env python3

# import array
# import struct
# import socket
# import fcntl
#
# SIOCGIFCONF = 0x8912  #define SIOCGIFCONF
# BYTES = 4096          # Simply define the byte size
#
# # get_iface_list function definition
# # this function will return array of all 'up' interfaces
# def get_iface_list():
#     # create the socket object to get the interface list
#     sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
#     # prepare the struct variable
#     names = array.array('B', b'\0' * BYTES)
#
#     # the trick is to get the list from ioctl
#     bytelen = struct.unpack('iL', fcntl.ioctl(sck.fileno(), SIOCGIFCONF, struct.pack('iL', BYTES, names.buffer_info()[0])))[0]
#
#     # convert it to string
#     namestr = names.tostring()
#
#     # return the interfaces as array
#     return [namestr[i:i+32].split('\0', 1)[0] for i in range(0, bytelen, 32)]
#
# # now, use the function to get the 'up' interfaces array
# ifaces = get_iface_list()
#
# # well, what to do? print it out maybe...
# for iface in ifaces:
#     print(iface)

import netifaces
import ipaddress

# grab all interfaces like: lo, en0, en1, etc ...
ifs = netifaces.interfaces()

def printifs(interfaces, key, ipaddr):
        for i in interfaces[key]:
            ip = i['addr']
            ip = ip.split('%')[0]  # macos append %en0 at the end of address

            ipp = ipaddr(ip)
            if not ipp.is_loopback:
                print("Internet IP: {}  {}".format(ip, i[netifaces.AF_LINK]['addr']))


def printv4(i):
    printifs(i, netifaces.AF_INET, ipaddress.IPv4Address)


def printv6(i):
    printifs(i, netifaces.AF_INET6, ipaddress.IPv6Address)


for s in ifs:
    i =  netifaces.ifaddresses(s)

    # if netifaces.AF_LINK in i.keys():
    #     for ii in i[netifaces.AF_LINK]:
    #         ip = ii['addr']
    #         print("MAC: {}".format(ip))

    if netifaces.AF_INET in i.keys():
        printv4(i)


    if netifaces.AF_INET6 in i.keys():
        printv6(i)
