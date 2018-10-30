#!/usr/bin/env python
# -*- coding: utf-8 -*-
import msgpack
import gzip  # compression


# Define data
data = {'a list': [1, 42, 3.141, 1337, 'help'],
        'a string': 'bla',
        6: bytearray(range(255)),
        'another dict': {'foo': 'bar',
                         'key': 'value',
                         'the answer': 42}}

# compress gains me nothing, infact it is ALWAY bigger. Somethimes a little
# and sometimes a lot bigger
if False:
    filename = 'data2.msgpack'
    use_compression = True
else:
    filename = 'data.msgpack'
    use_compression = False

# Write msgpack file
if use_compression:
    with gzip.open(filename, 'wb') as f:
        b = msgpack.packb(data, use_bin_type=True)
        f.write(b)
else:
    with open(filename, 'w') as outfile:
        msgpack.pack(data, outfile)

# Read msgpack file
if use_compression:
    with gzip.open(filename, 'r') as f:
        b = f.read()
        data_loaded = msgpack.unpackb(b, use_list=False, raw=False)
else:
    with open(filename) as data_file:
        # data_loaded = json.load(data_file)
        data_loaded = msgpack.unpack(data_file)

print(data == data_loaded)
# print(data)
# print(data_loaded)
