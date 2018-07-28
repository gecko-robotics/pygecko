#!/usr/bin/env python3

# why?? well, just incase we launch python 2 instead
from __future__ import print_function, division
import time

# fix path for now
import sys
sys.path.append("../")

from pygecko.transport import GeckoCore


if __name__ == "__main__":
    core = GeckoCore()
    core.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
