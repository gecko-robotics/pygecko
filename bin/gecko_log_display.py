#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################
# 
from pygecko.transport import zmqTCP
from pygecko.multiprocessing import geckopy
from colorama import Fore, Back, Style
import time

def handleArgs():
    parser = argparse.ArgumentParser(description='Displays geckopy.log() data')
    parser.add_argument('--host', help='geckocore host, default is localhost', default='localhost')
    parser.add_argument('-t', '--topic', help='log topic name, default is "log"', default='log')
    args = vars(parser.parse_args())
    return args

def format_print(topic, msg):
    # msg format: {proc_name, level, text}
    if msg.level == b'DEBUG': color = Fore.CYAN
    elif msg.level == b'WARNING': color = Fore.YELLOW
    elif msg.level == b'ERROR': color = Fore.RED
    else: color = Fore.GREEN
    
    # shorten proc names??
    print(Style.BRIGHT + color + '>> {}:'.format(msg.name[:8]) + Style.RESET_ALL + msg.text)
    # print(">> {}: {}".format(topic, msg))

if __name__ == "__main__":
    args = handleArgs()
    topic = args['topic']
    
    host = args['host']
    kwargs = {
        'in_addr': zmqTCP(host, 9998),
        'out_addr': zmqTCP(host, 9999)
    }
    
    geckopy.init_node(**kwargs)
    geckopy.Subscriber([topic], format_print)
    geckopy.spin()
