#!/usr/bin/env python

from pygecko.bag import BagWriter, BagReader

if __name__ == "__main__":
    filename = "bob.bag"

    bw = BagWriter(buffer_size=100)  # make buffer small to for writing
    bw.open(filename)

    data = range(20)
    for d in data:
        bw.push(d)

    bw.close()

    br = BagReader()
    data_in = br.read_all(filename)

    print(data == data_in)
