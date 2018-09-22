#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2018 Kevin Walchko
# see LICENSE for full details
##############################################

def valid_json(data):
    try:
        json.loads(data)
        return True
    except Exception as e:
        print(e)
        return False


def handleArgs():
    parser = argparse.ArgumentParser(description='Use multicast to find a geckocore node on the network')
    parser.add_argument('--file', help='launch file to be validated')
    args = vars(parser.parse_args())
    return args


if __name__ == "__main__":
    args = handleArgs()

    with open(args['file']) as file:
        data = file.read()

    val = valid_json(json)

    print("")
    print(">> {} file is valid: {}".format(val))
    print("")
