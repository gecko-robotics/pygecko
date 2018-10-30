#!/usr/bin/env python

from pygecko.bag import BagWriter, BagReader

if __name__ == "__main__":
    filename = "bob.bag"

    bw = BagWriter(filename)  # make buffer small to for writing
    # bw.open(filename)

    data = range(100)
    for d in data:
        bw.push(d)

    bw.write()

    print("\n\n=====================================\n\n")

    br = BagReader()
    data_in = br.read_all(filename)

    print(data == data_in)
